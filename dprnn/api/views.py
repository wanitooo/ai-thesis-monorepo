import time  # for benchmarking purposes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status
from .serializers import AudioUploadSerializer
from rest_framework.viewsets import ViewSet
from dprnn.api.serializers import UserSerializer, GroupSerializer
from rest_framework import permissions
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from django.http import response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import sys
import os
sys.path.append(os.path.join(sys.path[0], 'dprnn', 'ai'))
sys.path.append(os.path.join(sys.path[0], 'dprnn', 'utils'))
# Do not change the order of the sys.path.append, from ai import .... must be below sys.path.append
# from test import Random
from ai import DRNNModel, DPRNNModel



class FileUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AudioUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # print(serializer.validated_data)
            # you can access the file like this from serializer
            # uploaded_file = serializer.validated_data["file"]
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )  # ViewSets define the view behavior.


class UploadViewSet(ViewSet):
    serializer_class = AudioUploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        file_uploaded = request.FILES.get('file_uploaded')
        if file_uploaded:
            print(file_uploaded)
            file_uploaded.save()

        content_type = file_uploaded.content_type
        response = "POST API and you have uploaded a {} file".format(
            content_type)
        return Response(response)
# Create your views here.


class DrnnSeparate(APIView):
    """
    Gets the separated audio of two given audio using Deep Clustering with DRNN.
    """
    def post(self, request):
        # print("Request ", request)
        results = DRNNModel.get_separated_audio(request)
        
        if results:
            return Response({"message": "Separation successful", "spk_1": results['spk_1'], "spk_2": results['spk_2']})
        return Response({"message": "Something went wrong"})


class DualRnnSeparate(APIView):
    """
    Gets the separated audio of two given audio using Deep Clustering with DPRNN.
    """
    def post(self, request):
        results = DPRNNModel.get_separated_audio(request)
        if results:
            return Response({"message": "Separation successful", "spk_1": results['spk_1'], "spk_2": results['spk_2']})
        return Response({"message": "Something went wrong"})

