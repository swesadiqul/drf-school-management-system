from django.db import transaction
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from decimal import Decimal
from django.contrib.auth import get_user_model
from .models.student import StudentAdmission, Student
from .models.parent import Parent
from .models.fees import Payment
from django.db import transaction


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
    print("Second Start")
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
            student.fees_payments.add(payment)
        except Student.DoesNotExist:
            print("Student Doesn't Exist")
            pass


# User = get_user_model()

# @receiver(post_save, sender=StudentAdmission)
# def create_student_and_payments(sender, instance, created, **kwargs):
#     if created:
#         student_user = User.objects.create(
#             email=instance.email,
#             is_active=True,
#             is_staff=True,
#             is_superuser=False,
#         )
#         student_user.set_password("use-!@#-123")
#         # student_user.save()
#         print("Student user created")

#         student = Student.objects.create(
#             user=student_user,
#             admission_history=instance,
#             current_class=instance.class_name,
#             current_section=instance.section_name,
#         )
#         print("Student created")
#         print("Student fees categories: ", instance.fees_categories.all())

#         for fees_category in instance.fees_categories.all():
#             payment = Payment.objects.create(
#                 amount=fees_category.amount,
#                 paid=Decimal('0.00'),  # Initial payment is 0
#                 fees_master=fees_category,
#                 status='Unpaid',  # Default status is unpaid
#             )
#             student.fees_payments.add(payment)

#             # Create parent user associated with the newly admit form
#             parent_user = User.objects.create(
#                 email=instance.guardian_email,
#                 is_active=True,
#                 is_staff=True,
#                 is_superuser=False,
#             )
#             parent_user.set_password("use-!@#-123")
#             parent_user.save()

#             # Create the associated parent
#             parent = Parent.objects.create(
#                 user=parent_user,
#                 student=student,
#             )
#             parent.save()
