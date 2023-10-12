from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class ListBusinessAdminSerializer(serializers.ModelSerializer):
    """
    Serializer for listing business administrators. This serializer includes necessary fields for admin details.
    """
    class Meta:
        model = CustomUser
        exclude = ('password', 'last_login', 'date_joined', 'groups', 'user_permissions', )
        

class ListBusinessBranchAdminSerializer(serializers.ModelSerializer):
    """
    Serializer for listing business branch administrators. This serializer includes necessary fields for admin details.
    """
    class Meta:
        model = CustomUser
        exclude = ('password', 'last_login', 'date_joined', 'groups', 'user_permissions', )
        