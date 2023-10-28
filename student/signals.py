from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from decimal import Decimal
from django.contrib.auth import get_user_model
from .models.student import StudentAdmission, Student
from .models.parent import Parent
from .models.fees import Payment
from .models.exam import ExamGroup, Exam


User = get_user_model()


@receiver(post_save, sender=StudentAdmission)
def create_student_and_student(sender, instance, created, **kwargs):
    if created:
        try:
            # Create student user associated with the newly admit form
            student_user = User.objects.create(
                email=instance.email,
                is_active=True,
                is_staff=True,
                is_superuser=False,
            )
            student_user.set_password("use-!@#-123")
            student_user.save()

            # Create the associated student
            student = Student.objects.create(
                user=student_user,
                admission_history=instance,
                current_class=instance.class_name,
                current_section=instance.section_name,
            )

            # Save the student instance
            student.save()

            # Create parent user associated with the newly admit form
            parent_user = User.objects.create(
                email=instance.guardian_email,
                is_active=True,
                is_staff=True,
                is_superuser=False,
            )
            parent_user.set_password("use-!@#-123")
            parent_user.save()

            # Create the associated parent
            parent = Parent.objects.create(
                user=parent_user,
                student=student,
            )
            parent.save()
            print("First Done")
        except Exception as e:
            print(f"An error occurred: {str(e)}")



# Update the existing signal to handle m2m changes
@receiver(m2m_changed, sender=StudentAdmission.fees_categories.through)
def update_student_fees_categories(sender, instance, action, model, pk_set, **kwargs):
    if action == "post_add":
        try:
            student = Student.objects.get(admission_history=instance)
            for fees_category in instance.fees_categories.all():
                payment = Payment.objects.create(
                    amount=fees_category.amount,
                    paid=Decimal('0.00'),  # Initial payment is 0
                    fees_master=fees_category,
                    status='Unpaid',  # Default status is unpaid
                )

                # Generate a unique payment_id
                if not payment.payment_id:
                    # Find the number of existing payment IDs with the same prefix
                    existing_payment_ids = Payment.objects.filter(payment_id__startswith=f"{payment.pay_id:03}").values_list('payment_id', flat=True)
                    count = existing_payment_ids.count()

                    # Create a unique three-digit payment ID
                    unique_payment_id = f"{payment.pay_id:03}"
                    while unique_payment_id in existing_payment_ids:
                        count += 1
                        unique_payment_id = f"{payment.pay_id:03}"

                    payment.payment_id = unique_payment_id
                    payment.save()

                student.fees_payments.add(payment)
        except Student.DoesNotExist:
            print("Student Doesn't Exist")
            pass
        

# Signal handler to update no_of_exam when exams are added or removed
@receiver(m2m_changed, sender=ExamGroup.exam.through)
def update_no_of_exam(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add' or action == 'post_remove':
        instance.no_of_exam = instance.exam.count()
        instance.save()
