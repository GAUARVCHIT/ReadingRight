from django.shortcuts import render
from rest_framework import generics,status,views
from .serializers import RegisterSerializers, LoginSerializer
from rest_framework.response import Response

#jwt
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError,force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from .renderers import UserRenderer
# Create your views here.

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializers
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        print('gaurav: ',user_data)

        user = User.objects.get(email=user_data['email'])

        return Response(user_data,status=status.HTTP_201_CREATED)

class LoginAPIView(generics.GenericAPIView):
     
    serializer_class = LoginSerializer
    def post(self,request):

        serializer = self.serializer_class(data = request.data)

        serializer.is_valid(raise_exception=True)

        return Response(serializer.data,status=status.HTTP_200_OK)


