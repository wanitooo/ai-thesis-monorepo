import os
import datetime
import re
import nltk
import ktrain
import pandas as pd
from pycontractions import Contractions

# from nltk.tokenize import sent_tokenize

class DRNNModel:
    @staticmethod
    def preload(*args):
        """
            Does the preloading of the Deep Clustering with DRNN model.
            Requires the existence of the models within specific directories (which can be seen below)
        """
        global dpcl_drnn
        # TODO: Preloading logic using Pytorch UwU
        
    @staticmethod
    def get_separated_audio(audio_1, audio_2):
        # TODO: Create separated audio logic using DPCL DRNN'
        return None
        
    @staticmethod
    def get_transcript(audio_1, audio_2):
        # TODO: Create transcript of the separated audios
        return None
    
    @staticmethod
    def get_WER(audio_1, audio_2):
        # TODO: Get WER scrores of the separated audios
        return None    
    def get_SI_SNR(audio_1, audio_2):
        # TODO: Get SI_SNR scrores of the separated audios
        return None        
        
class Models:

    @staticmethod
    def preload(*args):
        """
            Does the preloading of the prediction models and the contraction models.
            Requires the existence of the models within specific directories (which can be seen below)

            Warning: may consume much RAM (around 1-2 gb for each model plus around 300-400 mb for the contractions), it is highly recomended to preload ONLY the models you will use to test a module to speed up loading and save resources.

            Possible Arguments:
                "Contrations": Preload pycontractions model
                "Predictors": Preload ktrain predictors models

            Module Prerequisites:
            - Text Preprocessing needs "Contractions".
            - Personality Prediction needs "Contractions", "Predictors".
        """
        print("aiquire.ulrs: ai.Models.preload()")
        print("Warning: may consume much RAM (around 1-2 gb for each model plus around 300-400 mb for the contractions), it is highly recomended to preload ONLY the models you will use to test a module to speed up loading and save resources.")

        global cont

        global agr_predictor
        global con_predictor
        global ext_predictor
        global neu_predictor
        global opn_predictor

        for argument in args:
            if argument == "Contractions":
                # CONTRACTIONS BLOCK
                print("Loading Contractions")

                # This section is necessary for normalization of contractions.
                # Choose model accordingly for contractions function
                # Reference: https://github.com/ian-beaver/pycontractions/tree/master/pycontractions
                cont = Contractions(api_key="glove-twitter-100")
                cont.load_models()

            elif argument == "Predictors":
                # PREDICTION BLOCK
                print("Loading Saved Predictors")

                # this is assuming that the models are contained within the provided directory names
                # and that they are outside the personality_prediction directory
                con_predictor = ktrain.load_predictor(
                    '../../personality-prediction-models/CON_predictor/Conscientiousness-predictor (essays)')
                ext_predictor = ktrain.load_predictor(
                    '../../personality-prediction-models/EXT_predictor/Extraversion-predictor (essays)')
                neu_predictor = ktrain.load_predictor(
                    '../../personality-prediction-models/NEU_predictor/Neuroticism-predictor (essays)')
                opn_predictor = ktrain.load_predictor(
                    '../../personality-prediction-models/OPN_predictor/Openness-predictor (essays)')
                agr_predictor = ktrain.load_predictor(
                    '../../personality-prediction-models/AGR_predictor/Agreeableness-predictor (essays)')

            # # PREREQUISITES FOR TRAINING
            # elif argument == "Something"
            #   # CODES HERE IF NEEDED

            else:
                raise Exception("Invalid Argument: " + argument)

        # needed submodules for NLP-related functions
        nltk.download('punkt')
        nltk.download('wordnet')

        # debugging statement
        print("Loading Complete")

    @staticmethod
    def get_prediction_probability(transcript):
        """
            Gets the prediction probability of a given post/transcript based on the five models.

            Parameters:
            -------------
            string my_post: represents the post/transcript which will undergo prediction

            Returns:
            -------------
            a dictionary containing the different probabilities grouped by model name 
        """

        # cleaned_json = Models.extract_text(my_post)
        val = Preprocess.preprocess(transcript)
        agr = agr_predictor.predict_proba(val).tolist()
        ext = ext_predictor.predict_proba(val).tolist()
        con = con_predictor.predict_proba(val).tolist()
        neu = neu_predictor.predict_proba(val).tolist()
        opn = opn_predictor.predict_proba(val).tolist()
        return {"agr": agr, "con": con, "ext": ext, "neu": neu, "opn": opn}


class Preprocess:

    @staticmethod
    def punctuation(string):
        """
        Removes punctuation and applies lowercase to the text

        Parameters:
        -----------
        string: Input string

        Returns:
        -----------
        string: Lowercased output string without punctuation

        """
        # added full stops (.?!) as they might have forgotten to add it
        # punctuation marks
        punctuations = '''"#$%&\()*+,‘“”’-/:;<=>_@[\\]^`{|}~'''
        for x in string.lower():
            if x in punctuations:
                string = string.replace(x, " ")
        return string

    @staticmethod
    def extract_text(transcripts):
        """
         Description:
        Extract "text" from trascript JSONN

        Parameters:
        <List> transcripts: An array of transcript

        Returns:
        <str> unprocessed_text: Concatenated string of "text" keys in transcript JSON
       """
        unprocessed_text = ""
        for transcript in transcripts['transcript']:
            unprocessed_text += transcript["text"] + " "

        return unprocessed_text

    @staticmethod
    def preprocess(text):
        """
        Description:
        - Removes Hyperlinks
        - Removes Punctuations and symbols(e.g. '+,@>=) exepct sentence identifier (e.g. ?!.)
        - Convert Extra fullstops and extra whitespace to period (e.g. ??? to ?, ... to .)
        - Expand contractions (e.g. don't => do not)


        Parameters:
        text: Raw transcription string

        Returns:
        <str>: Lowercased output string that may contain [? ! .] special characters 

        """

        # Load as panda array
        df1 = pd.DataFrame([text])
        df1.columns = ['TEXT']

        # Remove all hyperlinks (e.g. http://www.google.com)
        df1['TEXT'] = df1['TEXT'].apply(
            lambda x: re.sub(r'http\S+|\s\s\S+', '', x))

        # Removing punctuations except sentence identifiers (e.g. ?!.')
        # Identifiers are needed at this part of processing as we need stoppers
        df1['TEXT'] = df1['TEXT'].apply(Preprocess.punctuation)

        # Removing extra whitespaces and replacing with only one
        df1['TEXT'] = df1['TEXT'].apply(lambda a: re.sub('\s\s+', ' ', a))

        # Removing extra fullstops and replacing with only one (e.g. ??? to ?, ... to .)
        df1['TEXT'] = df1['TEXT'].apply(lambda a: re.sub(r'\?+', "? ", a))
        df1['TEXT'] = df1['TEXT'].apply(lambda a: re.sub(r'\s\.+', ".", a))
        df1['TEXT'] = df1['TEXT'].apply(lambda a: re.sub(r'\.+', ". ", a))
        df1['TEXT'] = df1['TEXT'].apply(lambda a: re.sub(r'\!+', "! ", a))

        # Removing extra whitespaces and replacing with only one
        df1['TEXT'] = df1['TEXT'].apply(lambda a: re.sub('\s\s+', ' ', a))

        # Apply Sentence Tokenization for expansion of contraction words
        df1['sent_tokens'] = df1['TEXT'].apply(nltk.tokenize.sent_tokenize)

        # For each sentences, apply normalization of contractions
        # Expand shortened words, (e.g. don't to do not)
        # Reference: https://github.com/ian-beaver/pycontractions
        df1['expanded_sent_tokens'] = df1['sent_tokens'].apply(
            lambda x: list(cont.expand_texts(x, precise=True)))

        # This section is for joining the sentence tokens
        df1['TEXT'] = df1['expanded_sent_tokens'].apply(lambda x: ' '.join(x))

        # Turn every character to lowercase (if applicable)
        df1['TEXT'] = df1['TEXT'].str.lower()

        # Convert panda array to <List> and return index 0 string
        return df1['TEXT'].tolist()[0]

    @staticmethod
    def expand_contractions(text):
        """
        Expand shortened words, (e.g. don't to do not)
        Reference: https://github.com/ian-beaver/pycontractions

        Parameters:
        -----------
        text: Input string

        Returns:
        -----------
        text: Normalized string 


        """
        # text = list(cont.expand_texts([text], precise=True))[0]
        # return text
        return list(cont.expand_texts([text], precise=True))