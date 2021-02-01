from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError,force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email','username','password']

    def validate(self, attrs):
        email = attrs.get('email','')
        username = attrs.get('username','')

        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric character')
        return attrs
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=255,min_length=3)
    password = serializers.CharField(max_length = 68, min_length = 6,write_only=True)
    username = serializers.CharField(max_length=225,min_length=3,read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self,obj):
        print('object: ',obj)
        user = User.objects.get(email=obj['email'])

        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh']
        }
    class Meta:
        model = User
        fields = ['email','password','username','tokens']

    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')

        user = auth.authenticate(email = email, password = password)
                
        if not user:
            raise AuthenticationFailed('Invalid credential, try again')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')

        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email':user.email,
            'username':user.username,
            'tokens': user.tokens(),
        }

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self,attrs):
        self.token = attrs['refresh']

        return attrs

    def save(self,**kwargs):

        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad token')