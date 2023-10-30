from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.serializers import Serializer, FileField
from .models import UploadedFile


class AudioUploadSerializer(serializers.ModelSerializer):
    # file_uploaded = FileField()

    class Meta:
        model = UploadedFile
        fields = ['file', 'uploaded_on']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
