from rest_framework import serializers
from ..models import CustomUser
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField(validators=[EmailValidator(message="Enter a valid email address.")])
    password = serializers.CharField()
    

class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for initiating a password reset.
    """
    email = serializers.EmailField(validators=[EmailValidator(message="Enter a valid email address.")])

class VerifyResetPasswordOTPSerializer(serializers.Serializer):
    """
    Serializer for verifying the OTP during the password reset process.
    """
    otp = serializers.CharField(required=True, write_only=True)   

class ResetPasswordConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming the password reset by providing a new password.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})