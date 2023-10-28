from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import UniqueConstraint
from django.core.validators import RegexValidator
from ..models.fees import FeesMaster, Payment


CustomUser = get_user_model()


class Session(models.Model):
    session_name = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{4}-\d{2}$',
                message='Session name must be in the format "YYYY-YY" (e.g., 2019-20).',
            ),
        ]
    )

    def __str__(self):
        return self.session_name


class Section(models.Model):
    section_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.section_name
    
    class Meta:
        unique_together = ('section_name',)


class Subject(models.Model):
    subject_code = models.CharField(max_length=20, unique=True)
    subject_name = models.CharField(max_length=100, unique=True)
    SUBJECT_TYPE_CHOICES = [
        ('theory', 'Theory'),
        ('practical', 'Practical'),
    ]
    subject_type = models.CharField(
        max_length=20, choices=SUBJECT_TYPE_CHOICES)

    def __str__(self):
        return self.subject_name
    
    class Meta:
        unique_together = ('subject_name', 'subject_code', )


class Class(models.Model):
    class_name = models.CharField(max_length=50, unique=True)
    sections = models.ManyToManyField('Section', related_name='classes')
    subjects = models.ManyToManyField('Subject', related_name='classes')

    def __str__(self):
        return self.class_name


class StudentAdmission(models.Model):
    admission_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    nationality = models.CharField(max_length=50)
    class_name = models.ForeignKey(
        'Class', on_delete=models.SET_NULL, null=True, blank=True)
    section_name = models.ForeignKey(
        'Section', on_delete=models.SET_NULL, null=True, blank=True)
    session_name = models.ForeignKey(
    'Session', on_delete=models.SET_NULL, null=True, blank=True)
    religion = models.CharField(max_length=50)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    previous_school = models.CharField(max_length=150)
    admission_status = models.CharField(max_length=50)
    fees_categories = models.ManyToManyField('FeesMaster', blank=True, related_name='admissions')
    guardian_name = models.CharField(max_length=150)
    guardian_relationship = models.CharField(max_length=50)
    guardian_email = models.EmailField(
        max_length=254, unique=True, blank=True, null=True)
    guardian_contact_number = models.CharField(max_length=15)
    admission_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Admission ID: {self.admission_id})"


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    admission_history = models.OneToOneField(
        StudentAdmission, on_delete=models.CASCADE, related_name='student', default=None, null=True, blank=True)
    current_class = models.ForeignKey(
        Class, on_delete=models.SET_NULL, null=True, blank=True)
    current_section = models.ForeignKey(
        Section, on_delete=models.SET_NULL, null=True, blank=True)
    current_session = models.ForeignKey(
    Session, on_delete=models.SET_NULL, null=True, blank=True)
    fees_payments = models.ManyToManyField('Payment', blank=True, related_name='student_payments')
    is_disable = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    reminder_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
    
    @staticmethod
    def get_payments_for_students(students):
        if isinstance(students, models.QuerySet):
            # If students is a queryset, return payments for all students in the queryset
            return Payment.objects.filter(student__in=students)
        elif isinstance(students, models.Model):
            # If students is a single student object, return payments for that student
            return students.fees_payments.all()
        else:
            raise ValueError("Invalid input. Expected a single student object or a queryset of student objects.")
    
    # def save(self, *args, **kwargs):
    #     # Check if is_disable is being set to True
    #     if self.is_disable:
    #         # Check if there's no existing DisableReason for this student
    #         if not self.disable_reasons.exists():
    #             # Create a DisableReason for this student
    #             disable_reason = DisableReason.objects.create(
    #                 disable_name="Default Disable Reason"
    #             )
    #             disable_reason.student.add(self)  # Associate this student
    #             disable_reason.save()
    #     else:
    #         # Check if the student is associated with a DisableReason
    #         try:
    #             disable_reason = self.disable_reasons.get()
    #             # If associated, remove the student from DisableReason
    #             disable_reason.student.remove(self)
    #             # If no more students are associated, delete the DisableReason
    #             if disable_reason.student.count() == 0:
    #                 disable_reason.delete()
    #         except DisableReason.DoesNotExist:
    #             # If no DisableReason is associated, do nothing
    #             pass

    #     super().save(*args, **kwargs)

class StudentCategory(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    student = models.ManyToManyField(Student, related_name='categories')

    def __str__(self):
        return self.category_name


class DisableReason(models.Model):
    disable_name = models.CharField(max_length=50)
    student = models.ManyToManyField(Student, related_name='disable_reasons')

    def __str__(self):
        return self.disable_name
    
    # class Meta:
    #     unique_together = ('disable_name', 'id', )


class PromoteStudents(models.Model):
    promotion_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    from_class = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name='from_class')
    to_class = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name='to_class')
    from_section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name='from_section')
    to_section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name='to_section')
    promotion_date = models.DateField(default=timezone.now)
    remarks = models.TextField()

    def __str__(self):
        return f"Promotion ID: {self.promotion_id} - Student: {self.student.user.email}"

    class Meta:
        # Ensure uniqueness for the combination of from_class and pk
        constraints = [
            UniqueConstraint(
                fields=['from_class', 'promotion_id'],
                name='unique_promote_from_class_promotion_id'
            ),
        ]
        # Add an index for from_class to improve search performance
        indexes = [
            models.Index(fields=['from_class']),
        ]



