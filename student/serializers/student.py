from rest_framework import serializers
from usermanager.models import CustomUser
from ..models.student import Student, StudentAdmission, Class, Section, PromoteStudents
from ..models.parent import Parent
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name',
                  'date_of_birth', 'profile_picture', 'is_active', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}


class SectionSerializer(serializers.ModelSerializer):
    """
    Serializer for Section model.
    """
    class Meta:
        model = Section
        fields = '__all__'


class ClassSerializer(serializers.ModelSerializer):
    """
    Serializer for Class model.
    """
    class Meta:
        model = Class
        fields = '__all__'


class StudentAdmissionSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentAdmission model.
    """
    class Meta:
        model = StudentAdmission
        fields = "__all__"

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format")
        return value

    def validate_contact_number(self, value):
        if len(value) != 11:
            raise serializers.ValidationError(
                "Contact number must be 11 digits")
        if not value.isdigit():
            raise serializers.ValidationError(
                "Contact number must contain only digits")
        return value

    def validate_guardian_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid guardian email format")
        return value

    def validate_guardian_contact_number(self, value):
        if len(value) != 11:
            raise serializers.ValidationError(
                "Guardian contact number must be 11 digits")
        if not value.isdigit():
            raise serializers.ValidationError(
                "Guardian contact number must contain only digits")
        return value


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for Student model.
    """
    user = CustomUserSerializer()
    current_class = ClassSerializer()
    current_section = SectionSerializer()
    admission_history = StudentAdmissionSerializer()

    class Meta:
        model = Student
        fields = "__all__"


class PromoteStudentSerializer(serializers.Serializer):
    """
    Serializer for PromoteStudents model.
    """
    student_id = serializers.IntegerField()
    to_class_id = serializers.IntegerField()
    to_section_id = serializers.IntegerField()
    remarks = serializers.CharField(required=False)

class PromoteAllStudentsSerializer(serializers.Serializer):
    """
    Serializer for PromoteStudents model.
    """
    from_class_id = serializers.IntegerField()
    to_class_id = serializers.IntegerField()
    to_section_id = serializers.IntegerField()
    remarks = serializers.CharField(required=False)
        



