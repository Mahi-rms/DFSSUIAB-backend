from .models import *
from rest_framework import serializers

class CredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
