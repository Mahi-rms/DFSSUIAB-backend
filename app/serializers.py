from .models import *
from rest_framework import serializers

class CredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

class FileUploadingSerializer(serializers.Serializer):
    class Meta:
        public_key=serializers.CharField()
        file_name=serializers.CharField()