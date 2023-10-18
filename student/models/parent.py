from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from .student import Student

CustomUser = get_user_model()

class Parent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student = models.OneToOneField(
        Student, on_delete=models.CASCADE, related_name='parent')
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.email