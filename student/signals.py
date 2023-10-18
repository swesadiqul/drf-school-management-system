from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models.student import StudentAdmission, Student
from .models.parent import Parent

User = get_user_model()

@receiver(post_save, sender=StudentAdmission)
def create_student_and_student(sender, instance, created, **kwargs):
    if created:
        
        # <<<<------   Student   ------>>>>
        
        # Create student user associated with the newly admit form
        
        student_user = User.objects.create(
            email=instance.email,
            is_active=True,
            is_staff=True,
            is_superuser=False,
        )
        student_user.set_password("use-!@#-123")
        student_user.save()
        
        # Create the associated parent
        student = Student.objects.create(
            user=student_user,
            admission_history=instance,
            current_class=instance.class_name,
            current_section=instance.section_name,
        )
        student.save()
        
         # <<<<------   Parent   ------>>>>

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
