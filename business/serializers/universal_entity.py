from rest_framework import serializers

from ..models import Business, Type, UniversalEntities


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class UniversalEntitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversalEntities
        fields = '__all__'
