from rest_framework import serializers
from ..models.fees import FeesGroup, FeesType, FeesDiscount, FeesMaster, FeesCollect, Payment
from ..serializers.student import StudentSerializer
from ..models.student import Student

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

    

class FeesTypeSearchSerializer(serializers.Serializer):
    students = StudentSerializer(many=True)
    

class StudentSerializer(serializers.ModelSerializer):
    class_name = serializers.ReadOnlyField(source='current_class.class_name')
    student_name = serializers.ReadOnlyField(source='user.get_full_name')

    class Meta:
        model = Student
        fields = ['id', 'class_name', 'student_name']
        

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class FeesCollectSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    payments = PaymentSerializer(many=True)
    