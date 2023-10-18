from rest_framework import serializers
from ..models.parent import Parent
from ..serializers.student import StudentSerializer, CustomUserSerializer

class ParentSerializer(serializers.ModelSerializer):
    """
    Serializer for Parent model.
    """
    user = CustomUserSerializer()
    student = StudentSerializer()

    class Meta:
        model = Parent
        fields = ['id', 'user', 'student', 'date_joined']