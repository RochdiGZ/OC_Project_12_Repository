# authentication/models.py
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """The CustomUserManager class inherits from BaseUserManager class."""
    def create_user(self, email, password=None, first_name=None, last_name=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set.')
        # Verify that email is valid with normalize_email method
        user = self.model(
            email=self.normalize_email(email).lower(),
            first_name=first_name.capitalize(),
            last_name=last_name.upper()
        )
        # Modify the password with set_password method
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, first_name=None, last_name=None, **extra_fields):
        user = self.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save()
        return user


class Employee(AbstractBaseUser, PermissionsMixin):
    """The Employee class inherits from AbstractBaseUser class."""
    ROLES_CHOICES = [('sales', 'sales'), ('support', 'support')]
    email = models.EmailField(max_length=128, unique=True, blank=False)
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    role = models.CharField(blank=False, null=False,
                            max_length=10, choices=ROLES_CHOICES)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = "Email User"
        verbose_name_plural = "Emails Users"

    def __str__(self):
        return self.email
