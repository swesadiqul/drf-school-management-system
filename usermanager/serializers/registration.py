
from rest_framework import serializers
from ..models import CustomUser
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator

CustomUser = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password2')

    def validate(self, attrs):
        """
        Validate the passwords to ensure they match.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs


class VerifyOTPSerializer(serializers.Serializer):
    """
    Serializer for OTP verification during user registration.
    """
    email = serializers.CharField(required=True)
    otp = serializers.CharField(required=True, write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'otp']
        
        
