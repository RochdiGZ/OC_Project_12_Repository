# authentication/models.py
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from permissions import create_groups, add_to_group
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """The CustomUserManager class inherits from BaseUserManager class."""
    def create_user(self, email, password, first_name=None, last_name=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set.')
        # Verify that email is valid with normalize_email method
        user = self.model(
            email=self.normalize_email(email).lower(),
            first_name=first_name.capitalize(),
            last_name=last_name.upper(),
            **extra_fields
        )
        # Modify the password with set_password method
        user.set_password(password)
        if user.is_superuser:
            user.role = 'manager'

        user.save()
        add_to_group(user)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
            Create and save a SuperUser with the given email and password.
        """
        if not Group.objects.filter(name='support'):
            create_groups()
        else:
            pass

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.get('role', 'manager')
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class Employee(AbstractBaseUser, PermissionsMixin):
    """The Employee class inherits from AbstractBaseUser class."""
    ROLES_CHOICES = [('sales', 'sales'), ('support', 'support'), ('manager', 'manager')]

    email = models.EmailField(max_length=128, unique=True, blank=False)
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    role = models.CharField(blank=False, null=False,
                            max_length=10, choices=ROLES_CHOICES)
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_set",
        related_query_name="user",
    )
    is_staff = models.BooleanField(default=True, editable=False)
    is_superuser = models.BooleanField(default=False, editable=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = "Employee"

    def __str__(self):
        return self.email
