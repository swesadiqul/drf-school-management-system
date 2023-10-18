from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class BaseUserProfile(models.Model):
    username = models.CharField(
        max_length=60, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', null=True, blank=True)

    class Meta:
        abstract = True


class CustomUser(AbstractBaseUser, PermissionsMixin, BaseUserProfile):
    email = models.EmailField(unique=True)

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name


class SuperAdmin(models.Model):
    business = models.ForeignKey('business.Business', on_delete=models.CASCADE, related_name="business",
                                 null=True, blank=True)

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    # branch
    is_create_branch = models.BooleanField(default=False)
    branch_limit = models.PositiveIntegerField(default=0)
    is_business_admin = models.BooleanField(default=False)
    is_branch_admin = models.BooleanField(default=False)

    # is_staff = models.BooleanField(default=True)
    # is_active = models.BooleanField(default=True)
    # is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.user.email
