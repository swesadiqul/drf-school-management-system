from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from student.models import Student, Parent

User = get_user_model()

@receiver(post_save, sender=Student)
def create_parent_for_student(sender, instance, created, **kwargs):
    if created:
        print(instance.parent_email)
        print(instance)
        # Create a user associated with the newly created student
        user = User.objects.create(
            email=instance.parent_email,
            is_active=True,
            is_staff=True,
            is_superuser=False,
        )

        # Set the user's password using set_password to ensure it's hashed
        user.set_password("use-!@#-123")
        user.save()

        # Create the associated parent
        parent = Parent.objects.create(
            user=user,
            student=instance,
        )
        parent.save()
