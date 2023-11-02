import os
import datetime
import re
# import nltk
# import ktrain
# import pandas as pd
# from pycontractions import Contractions
import sys, os
sys.path.append(os.path.join(sys.path[0],'dprnn','utils'))
# print(sys.path)

from dprnn.utils.separate import DRNNSeparation, DPRNNSeparation
# from nltk.tokenize import sent_tokenize


class DRNNModel:
    @staticmethod
    # def preload(*args):
    #     """
    #         Does the preloading of the Deep Clustering with DRNN model.
    #         Requires the existence of the models within specific directories (which can be seen below)
    #     """
    #     global dpcl_drnn
    #     dpcl_drnn = Separation(
                #  save_file='media/separated/', scp_file=separate_mix_scp)

    #     if dpcl_drnn:
    #         return Exception("Something went wrong, failed to pre-load model")
    #     return {"message": "successfully pre-loaded model"}

    def get_separated_audio(request):
        # TODO: Create separated audio logic using DPCL DRNN'
        separate_mix_scp = "dprnn/utils/mixed.scp" # creates file if not yet exists
        res = request.data
        # print("request.POST", request.POST)
        # print("request.data", request.data)
        if res:
            # return Response(request.POST.get('file'))
            separate_mix = open(separate_mix_scp, 'w')
            for root, dirs, files in os.walk(os.path.join('media', 'mixed')):
                files.sort()
                for file in files:
                    if file == os.path.basename(request.data['file']):
                        separate_mix.write(file+" "+root+'/'+file)
                        separate_mix.write('\n')
                        separate_mix.close()
        with open(separate_mix_scp, 'r') as f:
            print('SCP file contents: ', f.read())
        print("Separating audio via DRNN")
        separation = DRNNSeparation(
                 save_file='media/separated/', scp_file=separate_mix_scp)
        audios = separation.run()
        return {"spk_1": audios[0], "spk_2": audios[1]}

    @staticmethod
    def get_transcript(audio_1, audio_2):
        # TODO: Create transcript of the separated audios
        return None

    @staticmethod
    def get_WER(audio_1, audio_2):
        # TODO: Get WER scrores of the separated audios
        return None

    @staticmethod
    def get_SI_SNR(audio_1, audio_2):
        # TODO: Get SI_SNR scrores of the separated audios
        return None

    @staticmethod
    def get_mix_audio(audio_1, audio_2):
        # TODO: Create audio mixing logic, not needed accdg to Frontend
        # audio_mix = dpcl_drnn.run(scp_file=f"{audio_1} {audio_2}")
        # return {"audio_mix": audio_mix}
        return None
        
class DPRNNModel:
    @staticmethod
    # def preload(*args):
    #     """
    #         Does the preloading of the Deep Clustering with DRNN model.
    #         Requires the existence of the models within specific directories (which can be seen below)
    #     """
    #     global dpcl_drnn
    #     dpcl_drnn = Separation(
                #  save_file='media/separated/', scp_file=separate_mix_scp)

    #     if dpcl_drnn:
    #         return Exception("Something went wrong, failed to pre-load model")
    #     return {"message": "successfully pre-loaded model"}

    def get_separated_audio(request):
        # TODO: Create separated audio logic using DPCL DRNN'
        separate_mix_scp = "dprnn/utils/mixed.scp" # creates file if not yet exists
        res = request.data
        if res:
            # return Response(request.POST.get('file'))
            separate_mix = open(separate_mix_scp, 'w')
            for root, dirs, files in os.walk(os.path.join('media', 'mixed')):
                files.sort()
                for file in files:
                    if file == os.path.basename(request.POST.get('file')):
                        separate_mix.write(file+" "+root+'/'+file)
                        separate_mix.write('\n')
                        separate_mix.close()
        with open(separate_mix_scp, 'r') as f:
            print('SCP file contents: ', f.read())
        print("Separating audio via DPRNN")
        separation = DPRNNSeparation(
                 save_file='media/separated/', scp_file=separate_mix_scp)
        audios = separation.run()
        return {"spk_1": audios[0], "spk_2": audios[1]}

    @staticmethod
    def get_transcript(audio_1, audio_2):
        # TODO: Create transcript of the separated audios
        return None

    @staticmethod
    def get_WER(audio_1, audio_2):
        # TODO: Get WER scrores of the separated audios
        return None

    @staticmethod
    def get_SI_SNR(audio_1, audio_2):
        # TODO: Get SI_SNR scrores of the separated audios
        return None

    @staticmethod
    def get_mix_audio(audio_1, audio_2):
        # TODO: Create audio mixing logic, not needed accdg to Frontend
        # audio_mix = dpcl_drnn.run(scp_file=f"{audio_1} {audio_2}")
        # return {"audio_mix": audio_mix}
        return None
   