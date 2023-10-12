import torch
from sklearn.cluster import KMeans
from . import AudioData
import numpy as np
from utils import util
import argparse
from . import model
from .stft_istft import STFT
import os
import librosa
import pickle
from tqdm import tqdm
# import soundfile as sf
from typing import List


class Separation(object):
    '''
        test deep clutsering model
        dpcl: model
        scp_file: path of scp file
        opt: parse(yml)
        waves: AudioData file
        kmeans: KMeans
        num_spks: speaker number

        ~SETTINGS~
        DPCL:
            num_layer: 2
            nfft: 129  # nfft/2+1
            hidden_cells: 600
            emb_D: 40
            dropout: 0
            bidirectional: true
            activation: Tanh

        audio_setting:
            window: hann
            nfft: 256
            window_length: 256
            hop_length: 64
            center: true
            is_mag: false # abs(tf-domain)
            is_log: false # log(tf-domain)
    '''

    def __init__(self, scp_file, opt, save_file='./results'):
        super(Separation, self).__init__()
        gpu = False
        if gpu:
            initial = model.DPCL(num_layer=2, nfft=2, hidden_cells=600,
                                 emb_D=40, dropout=0, bidirectional=True, activation='Tanh')
            self.dpcl = initial.cuda()
            self.device = torch.device(
                'cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(
                'cuda' if torch.cuda.is_available() else 'cpu')
            self.dpcl = initial
        # self.dpcl = dpcl
        ckp = torch.load('./checkpoint/DPCL_optim_jusper/best.pt',
                         map_location=self.device)
        self.dpcl.load_state_dict(ckp['model_state_dict'])
        self.dpcl.eval()
        self.waves = AudioData(scp_file, window='hann', nfft=256, window_length=256,
                               hop_length=64, center=False, is_mag=True, is_log=True)
        self.keys = AudioData(scp_file, window='hann', nfft=256, window_length=256,
                              hop_length=64, center=False, is_mag=True, is_log=True).wave_keys
        self.kmeans = KMeans(n_clusters=opt['num_spks'])
        self.num_spks = opt['num_spks']
        self.save_file = save_file
        self.opt = opt

    def _cluster(self, wave, non_silent):
        '''
            input: T x F
        '''
        # TF x D
        print("hi i got pass through")
        mix_emb = self.dpcl(torch.tensor(
            wave, dtype=torch.float32), is_train=False)

        mix_emb = mix_emb.detach().numpy()
        # N x D
        mix_emb = mix_emb[non_silent.reshape(-1)]
        # N
        mix_cluster = self.kmeans.fit_predict(mix_emb)
        targets_mask = []
        for i in range(self.num_spks):
            mask = ~non_silent
            mask[non_silent] = (mix_cluster == i)
            targets_mask.append(mask)

        return targets_mask

    def run(self):
        stft_settings = {'window': self.opt['audio_setting']['window'],
                         'nfft': self.opt['audio_setting']['nfft'],
                         'window_length': self.opt['audio_setting']['window_length'],
                         'hop_length': self.opt['audio_setting']['hop_length'],
                         'center': self.opt['audio_setting']['center']}

        stft_istft = STFT(**stft_settings)
        index = 0
        output_file_paths: List[str] = []
        for wave in tqdm(self.waves):
            # log spk_spectrogram
            EPSILON = np.finfo(np.float32).eps
            log_wave = np.log(np.maximum(np.abs(wave), EPSILON))

            # apply cmvn
            cmvn = pickle.load(open(self.opt['cmvn_file'], 'rb'))
            cmvn_wave = util.apply_cmvn(log_wave, cmvn)

            # calculate non silent
            non_silent = util.compute_non_silent(log_wave).astype(np.bool)

            target_mask = self._cluster(cmvn_wave, non_silent)
            for i in range(len(target_mask)):
                name = self.keys[index]
                spk_spectrogram = target_mask[i] * wave
                i_stft = stft_istft.istft(spk_spectrogram)
                output_file = os.path.join(
                    self.save_file, self.opt['name'], 'spk'+str(i+1))
                os.makedirs(output_file, exist_ok=True)
                output_file_paths.append(output_file+'/'+name)
                librosa.output.write_wav(output_file+'/'+name, i_stft, 8000)
                # sf.write(output_file+'/'+name, i_stft, 8000)
            index += 1
        print('Processing {} utterances'.format(index))
        # return { audio_1: output_file_paths[0], audio_2: output_file_paths[1]}
