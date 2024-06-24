import noisereduce as nr
import sys
import os
sys.path.append('./')

import torch
from sklearn.cluster import KMeans
from dprnn.utils import AudioData
import numpy as np
from dprnn.utils import util
from dprnn.utils import model
from dprnn.utils.stft_istft import STFT
import os
import librosa
import pickle
from tqdm import tqdm
# import soundfile as sf
from typing import List

class DRNNSeparation(object):
    '''
        test deep clutsering model
        dpcl: model
        scp_file: path of scp file
        opt: parse(yml)
        waves: AudioData file
        kmeans: KMeans
        num_spks: speaker number
    '''

    def __init__(self, scp_file, save_file):
        super(DRNNSeparation, self).__init__()
        gpu = False
        # Simulates `dpcl = model.DPCL(**opt['DPCL'])`
        initial = model.DPCL(num_layer=2, nfft=129, hidden_cells=600,
                             emb_D=40, dropout=0, bidirectional=True, activation='Tanh')
        if gpu:

            self.dpcl = initial.cuda()
            self.device = torch.device(
                'cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(
                'cuda' if torch.cuda.is_available() else 'cpu')
            self.dpcl = initial
        ckp = torch.load('pretrained/drnn_jusper.pt',
                         map_location=self.device)
        self.dpcl.load_state_dict(ckp['model_state_dict'])
        self.dpcl.eval()
        self.waves = AudioData(scp_file, window='hann', nfft=256, window_length=256,
                               hop_length=64, center=False, is_mag=False, is_log=False)
        self.keys = AudioData(scp_file, window='hann', nfft=256, window_length=256,
                              hop_length=64, center=False, is_mag=False, is_log=False).wave_keys
        self.kmeans = KMeans(n_clusters=2)
        self.num_spks = 2
        self.save_file = save_file

    def _cluster(self, wave, non_silent):
        '''
            input: T x F
        '''
        # TF x D
        # print("hi i got pass through")
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
        stft_settings = {'window': 'hann',
                         'nfft': 256,
                         'window_length': 256,
                         'hop_length': 64,
                         'center': True}

        stft_istft = STFT(**stft_settings)
        index = 0
        output_file_paths = []
        for wave in tqdm(self.waves):
            # log spk_spectrogram
            EPSILON = np.finfo(np.float32).eps
            log_wave = np.log(np.maximum(np.abs(wave), EPSILON))

            # apply cmvn
            cmvn = pickle.load(open('dprnn/utils/cmvn.ark', 'rb'))
            cmvn_wave = util.apply_cmvn(log_wave, cmvn)

            # calculate non silent
            non_silent = util.compute_non_silent(log_wave).astype(np.bool)

            target_mask = self._cluster(cmvn_wave, non_silent)
            for i in range(len(target_mask)):
                name = self.keys[index]
                spk_spectrogram = target_mask[i] * wave
                i_stft = stft_istft.istft(spk_spectrogram)
                output_file = os.path.join(
                    self.save_file, "drnn",'spk'+str(i+1))
                os.makedirs(output_file, exist_ok=True)

                librosa.output.write_wav(output_file+'/'+name, i_stft, 8000)
                output_file_paths.append(output_file+'/'+name)
                # sf.write(output_file+'/'+name, i_stft, 8000)
            index += 1
        if index > 0:
            print('Processing {} utterances'.format(index))
            return output_file_paths
        else:
            print('Processing {} utterances'.format(index))
            return output_file_paths

class DPRNNSeparation(object):
    '''
        test deep clutsering model
        dpcl: model
        scp_file: path of scp file
        opt: parse(yml)
        waves: AudioData file
        kmeans: KMeans
        num_spks: speaker number
    '''

    def __init__(self, scp_file, save_file):
        super(DPRNNSeparation, self).__init__()
        gpu = False
        initial = model.DPCL_DPRNN(in_channels=129, hidden_channels=600, emb_D=10, dropout=0, rnn_type='LSTM', norm='gln', K=5,num_spks=2,
                            bidirectional=True, activation='Tanh', num_layers=1)
        if gpu:

            self.dpcl = initial.cuda()
            self.device = torch.device(
                'cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(
                'cuda' if torch.cuda.is_available() else 'cpu')
            self.dpcl = initial
        ckp = torch.load('pretrained/dprnn_best.pt',
                         map_location=self.device)
        self.dpcl.load_state_dict(ckp['model_state_dict'])
        self.dpcl.eval()
        self.waves = AudioData(scp_file, window='hann', nfft=256, window_length=256,
                               hop_length=64, center=False, is_mag=False, is_log=False)
        self.keys = AudioData(scp_file, window='hann', nfft=256, window_length=256,
                              hop_length=64, center=False, is_mag=False, is_log=False).wave_keys
        self.kmeans = KMeans(n_clusters=2)
        self.num_spks = 2
        self.save_file = save_file

    def _cluster(self, wave, non_silent):
        '''
            input: T x F
        '''
        # TF x D
        # print("hi i got pass through")
        mix_emb = self.dpcl(torch.tensor(
            wave, dtype=torch.float32), is_train=False)

        mix_emb = mix_emb.detach().numpy()
        # N x D
        mix_emb = mix_emb[non_silent.reshape(-1)]
        # N
        mix_cluster = self.kmeans.fit_predict(mix_emb)
        targets_mask = []
        for i in range(self.num_spks):
            mask = ~non_silent # negative of non_silent parts
            mask[non_silent] = (mix_cluster == i)
            targets_mask.append(mask)

        return targets_mask

    def run(self):
        stft_settings = {'window': 'hann',
                         'nfft': 256,
                         'window_length': 256,
                         'hop_length': 64,
                         'center': True}

        stft_istft = STFT(**stft_settings)
        index = 0
        output_file_paths = []
        for wave in tqdm(self.waves):
            # log spk_spectrogram
            EPSILON = np.finfo(np.float32).eps
            log_wave = np.log(np.maximum(np.abs(wave), EPSILON))

            # apply cmvn
            cmvn = pickle.load(open('dprnn/utils/cmvn.ark', 'rb'))
            cmvn_wave = util.apply_cmvn(log_wave, cmvn)

            # calculate non silent
            non_silent = util.compute_non_silent(log_wave).astype(np.bool)

            target_mask = self._cluster(cmvn_wave, non_silent)
            for i in range(len(target_mask)):
                name = self.keys[index]
                spk_spectrogram = target_mask[i] * wave
                i_stft = stft_istft.istft(spk_spectrogram)
                output_file = os.path.join(
                    self.save_file, "dprnn",'spk'+str(i+1))
                os.makedirs(output_file, exist_ok=True)
                file = nr.reduce_noise(
                    y=i_stft, sr=8000, prop_decrease=0.65)
                librosa.output.write_wav(
                    output_file+'/'+name, file, 8000)
                output_file_paths.append(output_file+'/'+name)
                # sf.write(output_file+'/'+name, i_stft, 8000)
            index += 1
        if index > 0:
            print('Processing {} utterances'.format(index))
            return output_file_paths
        else:
            print('Processing {} utterances'.format(index))
            return output_file_paths
    
if __name__ == "__main__":
    # parser = argparse.ArgumentParser(
    #     description='Parameters for testing Deep Clustering')
    # parser.add_argument('-scp', type=str, help='Path to option scp file.')
    # parser.add_argument('-opt', type=str,
    #                     help='Path to option YAML file.')
    # parser.add_argument('-save_file', type=str,
    #                     help='Path to save file.')
    # args = parser.parse_args()
    # opt = option.parse(args.opt)
    # dpcl = model.DPCL(**opt['DPCL'])

    separation = Separation(
        scp_file='dprnn/utils/mixed.scp', save_file='./result')
    separation.run()
