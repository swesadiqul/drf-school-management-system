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


class PaymentDetailsSerializer(serializers.Serializer):
    payment_id = serializers.CharField(max_length=6)
    collect_at = serializers.DateTimeField()
    student_name = serializers.SerializerMethodField()
    class_name = serializers.SerializerMethodField()
    fees_type = serializers.SerializerMethodField()
    payment_mode = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, allow_null=True)
    fine = serializers.DecimalField(
        max_digits=10, decimal_places=2, allow_null=True)

    class Meta:
        model = FeesCollect
        fields = ['payment_id', 'collect_at', 'payment_mode',
                  'amount', 'discount_amount', 'fine']

    def get_student_name(self, obj):
        pay_id = obj.payment_id[:3]
        student = Student.objects.filter(
            fees_payments__payment_id=pay_id).first()
        if student:
            return student.user.get_full_name() if student.user else None
        return None

    def get_class_name(self, obj):
        pay_id = obj.payment_id[:3]
        student = Student.objects.filter(
            fees_payments__payment_id=pay_id).first()
        if student:
            return student.current_class.class_name if student.current_class else None
        return None

    def get_fees_type(self, obj):
        pay_id = obj.payment_id[:3]
        payment = Payment.objects.filter(payment_id=pay_id).first()
        if payment:
            fees_type = payment.fees_master
            return str(fees_type)
        return None


class FeesDueMessageSentSerializer(serializers.Serializer):
    class_name = serializers.SerializerMethodField()
    section_name = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    student_email = serializers.SerializerMethodField()
    message = serializers.CharField(allow_null=True)

    def get_class_name(self, obj):
        return obj.current_class.class_name if obj.current_class else None

    def get_section_name(self, obj):
        return obj.current_section.section_name if obj.current_section else None

    def get_student_name(self, obj):
        return obj.user.get_full_name() if obj.user else None

    def get_student_email(self, obj):
        return obj.user.email if obj.user else None
