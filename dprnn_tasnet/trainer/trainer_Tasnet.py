from torch.nn.parallel import data_parallel
import matplotlib.pyplot as plt
import os
import torch
from model.loss import Loss
from logger.set_logger import setup_logger
import logging
import time
from utils.util import check_parameters
import sys
sys.path.append('../')


class Trainer(object):
    def __init__(self, train_dataloader, val_dataloader, Conv_Tasnet,  optimizer, scheduler, opt):
        super(Trainer).__init__()
        self.train_dataloader = train_dataloader
        self.val_dataloader = val_dataloader
        self.scheduler = scheduler
        self.num_spks = opt['num_spks']
        self.cur_epoch = 0
        self.total_epoch = opt['train']['epoch']
        self.early_stop = opt['train']['early_stop']

        self.print_freq = opt['logger']['print_freq']
        # setup_logger(opt['logger']['name'], opt['logger']['path'],
        #             screen=opt['logger']['screen'], tofile=opt['logger']['tofile'])
        self.logger = logging.getLogger(opt['logger']['name'])
        self.checkpoint = opt['train']['path']
        self.name = opt['name']

        if opt['train']['gpuid']:
            self.logger.info('Load Nvida GPU .....')
            self.device = torch.device(
                'cuda:{}'.format(opt['train']['gpuid'][0]))
            self.gpuid = opt['train']['gpuid']
            self.convtasnet = Conv_Tasnet.to(self.device)
            self.logger.info(
                'Loading Conv-TasNet parameters: {:.3f} Mb'.format(check_parameters(self.convtasnet)))
        else:
            self.gpuid = False
            self.logger.info('Load CPU ...........')
            self.device = torch.device('cpu')
            self.convtasnet = Conv_Tasnet.to(self.device)
            self.logger.info(
                'Loading Conv-TasNet parameters: {:.3f} Mb'.format(check_parameters(self.convtasnet)))

        if opt['resume']['state']:
            ckp = torch.load(opt['resume']['path'], map_location='cpu')
            self.cur_epoch = ckp['epoch']
            self.logger.info("Resume from checkpoint {}: epoch {:.3f}".format(
                opt['resume']['path'], self.cur_epoch))
            self.convtasnet = Conv_Tasnet.load_state_dict(
                ckp['model_state_dict']).to(self.device)
            self.optimizer = optimizer.load_state_dict(ckp['optim_state_dict'])
        else:
            self.convtasnet = Conv_Tasnet.to(self.device)
            self.optimizer = optimizer

        if opt['optim']['clip_norm']:
            self.clip_norm = opt['optim']['clip_norm']
            self.logger.info(
                "Gradient clipping by {}, default L2".format(self.clip_norm))
        else:
            self.clip_norm = 0

    def train(self, epoch):
        self.logger.info(
            'Start training from epoch: {:d}, iter: {:d}'.format(epoch, 0))
        self.convtasnet.train()
        num_batchs = len(self.train_dataloader)
        total_loss = 0.0
        num_index = 1
        start_time = time.time()
        for mix, ref in self.train_dataloader:
            mix = mix.to(self.device)
            ref = [ref[i].to(self.device) for i in range(self.num_spks)]
            self.optimizer.zero_grad()

            if self.gpuid:
                model = torch.nn.DataParallel(self.convtasnet)

                out = model(mix)
                # out = self.convtasnet(mix)
            else:
                out = self.convtasnet(mix)

            l = Loss(out, ref)
            epoch_loss = l
            total_loss += epoch_loss.item()
            epoch_loss.backward()

            if self.clip_norm:
                torch.nn.utils.clip_grad_norm_(
                    self.convtasnet.parameters(), self.clip_norm)

            self.optimizer.step()
            if num_index % self.print_freq == 0:
                message = '<epoch:{:d}, iter:{:d}, lr:{:.3e}, loss:{:.3f}>'.format(
                    epoch, num_index, self.optimizer.param_groups[0]['lr'], total_loss/num_index)
                self.logger.info(message)
            num_index += 1
        end_time = time.time()
        total_loss = total_loss/num_index
        message = 'Finished *** <epoch:{:d}, iter:{:d}, lr:{:.3e}, loss:{:.3f}, Total time:{:.3f} min> '.format(
            epoch, num_index, self.optimizer.param_groups[0]['lr'], total_loss, (end_time-start_time)/60)
        self.logger.info(message)
        return total_loss

    def validation(self, epoch):
        self.logger.info(
            'Start Validation from epoch: {:d}, iter: {:d}'.format(epoch, 0))
        self.convtasnet.eval()
        num_batchs = len(self.val_dataloader)
        num_index = 1
        total_loss = 0.0
        start_time = time.time()
        with torch.no_grad():
            for mix, ref in self.val_dataloader:
                mix = mix.to(self.device)
                ref = [ref[i].to(self.device) for i in range(self.num_spks)]
                self.optimizer.zero_grad()

                if self.gpuid:
                    # model = torch.nn.DataParallel(self.convtasnet)
                    # out = model(mix)
                    out = torch.nn.parallel.data_parallel(
                        self.convtasnet, mix, device_ids=self.gpuid)
                    out = self.convtasnet(mix)
                else:
                    out = self.convtasnet(mix)

                l = Loss(out, ref)
                epoch_loss = l
                total_loss += epoch_loss.item()
                if num_index % self.print_freq == 0:
                    message = '<epoch:{:d}, iter:{:d}, lr:{:.3e}, loss:{:.3f}>'.format(
                        epoch, num_index, self.optimizer.param_groups[0]['lr'], total_loss/num_index)
                    self.logger.info(message)
                num_index += 1
        end_time = time.time()
        total_loss = total_loss/num_index
        message = 'Finished *** <epoch:{:d}, iter:{:d}, lr:{:.3e}, loss:{:.3f}, Total time:{:.3f} min> '.format(
            epoch, num_index, self.optimizer.param_groups[0]['lr'], total_loss, (end_time-start_time)/60)
        self.logger.info(message)
        return total_loss

    def run(self):
        train_loss = []
        val_loss = []
        if self.gpuid and torch.cuda.is_available():
            torch.cuda.set_device(self.gpuid[0])
        else:
            # Pytorch defaults calculations to CPU when
            device = torch.device(self.device)
        # with torch.cuda.device(self.gpuid[0]): # Deleted the with block, incompatible with cpu code
        # Should still work with gpu? else put back with block
        self.save_checkpoint(self.cur_epoch, best=False)
        v_loss = self.validation(self.cur_epoch)
        best_loss = v_loss
        # self.logger.info("Current device", self.device)
        self.logger.info("Starting epoch from {:d}, loss = {:.4f}".format(
            self.cur_epoch, best_loss))
        no_improve = 0
        # starting training part
        while self.cur_epoch < self.total_epoch:
            self.cur_epoch += 1
            t_loss = self.train(self.cur_epoch)
            v_loss = self.validation(self.cur_epoch)

            train_loss.append(t_loss)
            val_loss.append(v_loss)

            # schedule here
            self.scheduler.step(v_loss)

            if v_loss >= best_loss:
                no_improve += 1
                self.logger.info(
                    'No improvement, Best Loss: {:.4f}'.format(best_loss))
            else:
                best_loss = v_loss
                no_improve = 0
                self.save_checkpoint(self.cur_epoch, best=True)
                self.logger.info('Epoch: {:d}, Now Best Loss Change: {:.4f}'.format(
                    self.cur_epoch, best_loss))

            if no_improve == self.early_stop:
                self.logger.info(
                    "Stop training cause no impr for {:d} epochs".format(
                        no_improve))
                break
        self.save_checkpoint(self.cur_epoch, best=False)
        self.logger.info("Training for {:d}/{:d} epoches done!".format(
            self.cur_epoch, self.total_epoch))

        # draw loss image
        plt.title("Loss of train and test")
        x = [i for i in range(self.cur_epoch)]
        plt.plot(x, train_loss, 'b-', label=u'train_loss', linewidth=0.8)
        plt.plot(x, val_loss, 'c-', label=u'val_loss', linewidth=0.8)
        plt.legend()
        # plt.xticks(l, lx)
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.savefig('loss.png')

    def save_checkpoint(self, epoch, best=True):
        '''
           save model
           best: the best model
        '''
        os.makedirs(os.path.join(self.checkpoint, self.name), exist_ok=True)
        torch.save({
            'epoch': epoch,
            'model_state_dict': self.convtasnet.state_dict(),
            'optim_state_dict': self.optimizer.state_dict()
        },
            os.path.join(self.checkpoint, self.name, '{0}.pt'.format('best' if best else 'last')))
