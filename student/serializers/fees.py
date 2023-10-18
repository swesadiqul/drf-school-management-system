from rest_framework import serializers
from ..models.fees import FeesGroup, FeesType, FeesDiscount, FeesMaster

class FeesGroupSerializer(serializers.ModelSerializer):
    """
    Serializer for FeesGroup model.
    """
    class Meta:
        model = FeesGroup
        fields = '__all__'
        optional_fields = ['description']

class FeesTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for FeesType model.
    """
    class Meta:
        model = FeesType
        fields = '__all__'
        optional_fields = ['description']

class FeesDiscountSerializer(serializers.ModelSerializer):
    """
    Serializer for FeesDiscount model.
    """
    class Meta:
        model = FeesDiscount
        fields = '__all__'
        optional_fields = ['description']

class FeesMasterSerializer(serializers.ModelSerializer):
    """
    Serializer for FeesMaster model.
    """
    class Meta:
        model = FeesMaster
        fields = '__all__'
