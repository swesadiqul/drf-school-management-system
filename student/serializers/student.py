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
        


class StudentListClsSecSerializer(serializers.ModelSerializer):
    class_name = serializers.SerializerMethodField()
    section_name = serializers.SerializerMethodField()
    admission_id = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['class_name', 'section_name', 'admission_id', 'full_name', 'email']

    def get_class_name(self, obj):
        return obj.current_class.class_name if obj.current_class else None

    def get_section_name(self, obj):
        return obj.current_section.section_name if obj.current_section else None

    def get_admission_id(self, obj):
        return obj.admission_history.admission_id if obj.admission_history else None

    def get_full_name(self, obj):
        return obj.user.get_full_name() if obj.user else None

    def get_email(self, obj):
        return obj.user.email if obj.user else None