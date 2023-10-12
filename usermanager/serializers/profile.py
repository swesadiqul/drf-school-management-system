
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing a user's password.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        """
        Validate the new password and confirm password.
        """
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("The new password and confirm password do not match.")
        return data
    
    
    