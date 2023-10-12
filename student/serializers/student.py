from rest_framework import serializers
from usermanager.models import CustomUser
from ..models import Student, Parent

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name', 'date_of_birth', 'profile_picture', 'is_active', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}


class StudentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(write_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'parent_email', 'gender', 'country', 'date_joined']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        
        # Access the email and password from the nested dictionary
        if user_data:
            email = user_data.get('email', None)
            password = user_data.get('password', None)

        # Create a CustomUser instance
        user = CustomUser.objects.create(email=email)
        user.set_password(password)
        user.save()

        student = Student.objects.create(user=user, **validated_data)
        return student
    
    