
from rest_framework import serializers
from django.core.exceptions import ValidationError

from ..models import Business, Type

class CreateBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        exclude = ('id', 'slug', 'is_active', 'created_at', 'updated_at')

    def validate_logo(self, value):
        # Ensure the file is an image
        if not value.content_type.startswith('image'):
            raise ValidationError("Only image files are allowed.")

        # Limit file size to 5 MB
        max_size = 5 * 1024 * 1024  # 5 MB in bytes
        if value.size > max_size:
            raise ValidationError("File size exceeds 5 MB.")

        return value
    
    def validate_email(self, value):
        if Business.objects.filter(email=value).exists():
            raise ValidationError("Business with this email already exists.")
        return value
    
    def validate_slug(self, value):
        if Business.objects.filter(slug=value).exists():
            raise ValidationError("Business with this slug already exists.")
        return value

    def create(self, validated_data):
        return Business.objects.create(**validated_data)
    
    
class ListBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        exclude = ('created_at', 'updated_at', 'is_active', )

class CreateBusinessBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        exclude = ('id', 'slug', 'is_active', 'created_at', 'updated_at', 'has_branch', 'branch_num', )

    def validate_logo(self, value):
        # Ensure the file is an image
        if not value.content_type.startswith('image'):
            raise ValidationError("Only image files are allowed.")

        # Limit file size to 5 MB
        max_size = 5 * 1024 * 1024  # 5 MB in bytes
        if value.size > max_size:
            raise ValidationError("File size exceeds 5 MB.")

        return value
    
    def validate_email(self, value):
        if Business.objects.filter(email=value).exists():
            raise ValidationError("Business with this email already exists.")
        return value
    
    def validate_slug(self, value):
        if Business.objects.filter(slug=value).exists():
            raise ValidationError("Business with this slug already exists.")
        return value

    def create(self, validated_data):
        return Business.objects.create(**validated_data)
    
    
class BusinessBranchesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        exclude = ('id', 'slug', 'is_active', 'created_at', 'updated_at', 'has_branch', 'branch_num', )
        