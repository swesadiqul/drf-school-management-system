from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
# from ..models.student import Class, Section
from django.core.validators import MinValueValidator


class FeesGroup(models.Model):
    group_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.group_name


class FeesType(models.Model):
    type_name = models.CharField(max_length=50, unique=True)
    fee_code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.type_name


class FeesDiscount(models.Model):
    discount_name = models.CharField(max_length=50,  unique=True)
    discount_code = models.CharField(max_length=50,  unique=True)
    DISCOUNT_TYPE_CHOICES = [
        ('Fixed', 'Fixed'),
        ('Percentage', 'Percentage'),
    ]
    discount_type = models.CharField(
        max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.discount_name

    def save(self, *args, **kwargs):
        if self.discount_type == 'Fixed':
            self.discount_percentage = None
            if self.discount_amount is None:
                raise ValidationError(
                    'Discount amount is required for Fixed discount type.')
        elif self.discount_type == 'Percentage':
            self.discount_amount = None
            if self.discount_percentage is None:
                raise ValidationError(
                    'Discount percentage is required for Percentage discount type.')

        super().save(*args, **kwargs)


class FeesMaster(models.Model):
    fees_group = models.ForeignKey(FeesGroup, on_delete=models.CASCADE)
    fees_type = models.ForeignKey(FeesType, on_delete=models.CASCADE)
    class_association = models.ManyToManyField(
        'Class', related_name='fees_masters')
    due_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    FINE_TYPE_CHOICES = [
        (None, 'None'),
        ('Percentage', 'Percentage'),
        ('Fixed', 'Fixed'),
    ]
    fine_type = models.CharField(
        max_length=20, choices=FINE_TYPE_CHOICES, default=None, null=True, blank=True)
    fine_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    fine_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.fees_type} - {self.fees_group}"

    @classmethod
    def get_fees_type_by_id(cls, fees_type_id):
        try:
            return cls.fees_type.objects.get(id=fees_type_id)
        except FeesType.DoesNotExist:
            return None

    @classmethod
    def get_all_fees_types_in_group(cls, fees_master_id):
        try:
            fees_master = cls.objects.get(id=fees_master_id)
            group_id = fees_master.fees_group.id
            return FeesType.objects.filter(fees_group_id=group_id)
        except FeesMaster.DoesNotExist:
            return None

    def save(self, *args, **kwargs):
        # Fine type is 'None'
        if self.fine_type == None:
            self.fine_amount = None
            self.fine_percentage = None
        # Fine type is 'Percentage'
        elif self.fine_type == 'Percentage':
            self.fine_amount = None
            if self.fine_percentage is None:
                raise ValueError(
                    "Fine percentage is required when fine type is 'Percentage'.")
        # Fine type is 'Fixed'
        elif self.fine_type == 'Fixed':
            self.fine_percentage = None
            if self.fine_amount is None:
                raise ValueError(
                    "Fine amount is required when fine type is 'Fixed'.")

        super().save(*args, **kwargs)


class Payment(models.Model):
    pay_id = models.AutoField(primary_key=True)
    payment_id = models.CharField(max_length=6, unique=True, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,  blank=True, validators=[MinValueValidator(0)], null=True)
    paid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)], default=0)

    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Partial', 'Partial'),
        ('Unpaid', 'Unpaid'),
    ]

    fees_master = models.ForeignKey(FeesMaster, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)], default=0)
    payment_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payment ID: , Status: {self.status}"


class FeesCollect(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount = models.ForeignKey(FeesDiscount, on_delete=models.CASCADE, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)], default=0)
    fine = models.DecimalField(max_digits=10, decimal_places=2, null=True, validators=[MinValueValidator(0)], blank=True)
    PAYMENT_MODE_CHOICES = [
        ('Cash', 'Cash'),
        ('DD', 'DD'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cheque', 'Cheque'),
        ('UPI', 'UPI'),
        ('Card', 'Card'),
    ]
    payment_mode = models.CharField(
        max_length=20, choices=PAYMENT_MODE_CHOICES)
    payment_id = models.CharField(max_length=6, unique=True, blank=True, null=True)
    collect_at = models.DateTimeField(default=timezone.now)
    note = models.TextField()

    def __str__(self):
        return f"Amount: {self.amount}, Payment Mode: {self.payment_mode}, Payment ID: {self.payment_id}"


class PaymentReminder(models.Model):
    reminder_id = models.AutoField(primary_key=True)
    # payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE)
    reminder_date = models.DateField()
    reminder_message = models.TextField()

    # def __str__(self):
    #     return f"Reminder ID: {self.reminder_id}, Payment ID: {self.payment_id}, Reminder Date: {self.reminder_date}"
