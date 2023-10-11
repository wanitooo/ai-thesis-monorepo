from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from dprnn.api.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
from django.http import response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from aiquire.ai import *
import time  # for benchmarking purposes

# Create your views here.


def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    print("Time Lapsed = {0}:{1}:{2}".format(int(hours), int(mins), sec))
    
class DrnnSeparate(APIView):
    """
    Gets the separated audio of two given audio using Deep Clustering with DRNN.
    """
class DPrnnSeparate(APIView):
    """
    Gets the separated audio of two given audio using Deep Clustering with DPRNN.
    """


class PredictProbability(APIView):
    """
        Gets the prediction probability of a given post/transcript based on the five models.
    """

    def post(self, request):
        """
            Gets the prediction probability of a given post/transcript based on the five models.

            Parameters:
            -------------
            string request.data['data']: represents the post/transcript 
            which will undergo prediction

            Returns:
            -------------
            a dictionary containing the different probabilities grouped by model name 
        """
        print("TIMING PERSONALITY")
        start = time.time()
        results = Models.get_prediction_probability(request.data['data'])
        agr = {"Critical": results['agr'][0], "Lenient": results['agr'][1]}
        con = {"Impulsive": results['con'][0], "Precise": results['con'][1]}
        ext = {"Extrovert": results['ext'][0], "Introvert": results['ext'][1]}
        neu = {"Even-tempered": results['neu']
               [0], "Temperamental": results['neu'][1]}
        opn = {"Conventional": results['opn']
               [0], "Insightful": results['opn'][1]}
        time_convert(time.time() - start)
        return Response({"Openness": opn, "Conscientiousness": con,
                         "Extraversion": ext, "Agreeableness": agr, "Neuroticism": neu})


class PredictPersonality(APIView):
    """
        Gets the personality classification of a given post/transcript based on the five models (based on the big 5 personality traits). Follows a binary classification based on the greater tuple value within a model's prediction.
    """

    def post(self, request):
        """
            Gets the personality classification of a given post/transcript based 
            on the five models (based on the big 5 personality traits). Follows a binary
            classification based on the greater tuple value within a model's prediction. 

            Parameters:
            -------------
            string request.data['data']: represents the post/transcript which will undergo prediction

            Returns:
            -------------
            a dictionary containing the big 5 personality classifications 
        """
        print("TIMING PERSONALITY")
        start = time.time()
        results = Models.get_prediction_probability(request.data['data'])
        opn_val = "Conventional" if results['opn'][0] > results['opn'][1] else "Insightful"
        con_val = "Impulsive" if results['con'][0] > results['con'][1] else "Precise"
        ext_val = "Extrovert" if results['ext'][0] > results['ext'][1] else "Introvert"
        agr_val = "Critical" if results['agr'][0] > results['agr'][1] else "Lenient"
        neu_val = "Even-tempered" if results['neu'][0] > results['neu'][1] else "Temperamental"
        time_convert(time.time() - start)
        return Response({"Openness": opn_val, "Conscientiousness": con_val,
                         "Extraversion": ext_val, "Agreeableness": agr_val, "Neuroticism": neu_val})


class CleanInput(APIView):
    """
        Simulates the cleaning of a post/transcript to prepare it for prediction.
    """

    def post(self, request):
        """
            Simulates the cleaning of a post/transcript to prepare it for prediction.

            Parameters:
            -------------
            string request.data['data']: represents the post/transcript which will undergo prediction

            Returns:
            -------------
            a cleaned string (lower case, without punctuations) 
        """
        print("TIMING CLEANINPUT")
        start = time.time()
        results = Preprocess.preprocess(request.data['data'])
        time_convert(time.time() - start)
        print(results)
        return Response(results)


class Preload(APIView):

    def get(self, request):
        Models.preload("Contractions", "Predictors")

        return Response(200)