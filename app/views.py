from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
from django.utils.decorators import method_decorator
from .serializers import *
from . import models
from hashlib import sha1
from rest_framework.response import Response
from helpers.api_helper import *
from helpers.authentication_helper import *
from helpers.auth_helper import login_required
from helpers.views_helper import *
from ecies.utils import generate_key
from ecies import encrypt, decrypt
import requests,os,json
import mimetypes,io
import calendar
import datetime
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
# Create your views here.
class Registration(APIView):
    @swagger_auto_schema(request_body=CredentialSerializer)
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            try:
                models.User.objects.get(email=email)
                return Response(api_response(ResponseType.FAILED, API_Messages.EMAIL_EXISTS), status=status.HTTP_400_BAD_REQUEST)
            except:
                user=models.User.objects.create(email=email,password=sha1(password.encode()).hexdigest())
                auth=AuthenticationHelper(user.id)
                auth_response = auth.authentication(user,password)
                if(not auth_response):
                    return Response(api_response(ResponseType.FAILED, API_Messages.INCORRECT_PASSWORD), status=status.HTTP_400_BAD_REQUEST)
                
                access_token = auth.generate_access_token()
                data = {
                    'user': user.id,
                    'email': user.email,
                    'access_token': access_token
                    }
                return Response(api_response(ResponseType.SUCCESS, API_Messages.SUCCESSFUL_REGISTRATION,data))
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    @swagger_auto_schema(request_body=CredentialSerializer)
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            try:
                user=models.User.objects.get(email=email)
                auth=AuthenticationHelper(user.id)
                auth_response = auth.authentication(user,password)
                if(not auth_response):
                    return Response(api_response(ResponseType.FAILED, API_Messages.INCORRECT_PASSWORD), status=status.HTTP_400_BAD_REQUEST)
                
                access_token = auth.generate_access_token()
                data = {
                    'user': user.id,
                    'email': user.email,
                    'access_token': access_token
                    }
                return Response(api_response(ResponseType.SUCCESS, API_Messages.SUCCESSFUL_LOGIN,data))
            except:
                return Response(api_response(ResponseType.FAILED, API_Messages.EMAIL_DOESNOT_EXIST))
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    def post(self, request):
        try:
            token = request.headers['Authorization'].split(" ")[-1]
            models.TokenBlackList.objects.create(token=token)
            return Response(api_response(ResponseType.SUCCESS, API_Messages.SUCCESSFUL_LOGOUT))
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)

class KeyGeneration(APIView):
    #Receiver Generates the Private Key and Public Keys and sends Public Key to Sender via any medium
    @method_decorator(login_required())
    def get(self,request):
        try:
            secp_k = generate_key()
            sk_bytes = secp_k.secret  #In bytes
            pk_bytes = secp_k.public_key.format(True)  #In bytes
            data={}
            data["private_key"]=sk_bytes.hex()
            data["public_key"]=pk_bytes.hex()
            return Response(api_response(ResponseType.SUCCESS, API_Messages.KEYS_GENERATED,data))
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)

class Uploading(APIView):
    # Sender Encrypts the file with Public Key of Receiver and Uploads it to IPFS and 
    # Sends IPFS hash to Receiver
    @method_decorator(login_required())
    def post(self,request):
        try:
            pk_bytes=request.data.get('pk_bytes')
            
            myfile = request.FILES['document']
            print(myfile.content_type(),dir(myfile))
            file=encrypt(pk_bytes,myfile.read())
            print("hey")
            res=requests.post("https://demo.storj-ipfs.com/api/v0/add",files={'upload_file':file}).text
            print("4")
            
            res=json.loads(res)
            print("5")
            print("6")
            data={}
            data["ipfs_hash"]=res['Hash']
            print("7")

            return Response(api_response(ResponseType.SUCCESS, API_Messages.FILE_UPLOADED,data))
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)
