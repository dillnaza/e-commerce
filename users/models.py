import uuid

from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            phone_number=phone_number,
            email=self.normalize_email(email),
            is_active=True, )

        user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, phone_number, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(phone_number=phone_number, email=email, password=password, )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = models.CharField(blank=True, null=True, max_length=1)
    email = models.EmailField(verbose_name=_("Email"), unique=True)
    phone_number = PhoneNumberField(unique=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return str(self.phone_number)
