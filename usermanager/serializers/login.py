from rest_framework import serializers
from ..models import CustomUser
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[EmailValidator(message="Enter a valid email address.")])
    password = serializers.CharField()
    

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[EmailValidator(message="Enter a valid email address.")])

class VerifyResetPasswordOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True, write_only=True)   

class ResetPasswordConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})