from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


CustomUser = get_user_model()

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    parent_email = models.EmailField(max_length=254, unique=True, blank=True, null=True)
    country = models.CharField(max_length=50,)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.email

class Parent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='parent')
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.email
    
    

