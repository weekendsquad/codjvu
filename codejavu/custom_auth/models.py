from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have a valid email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.email = email
        extra_fields.setdefault('is_pro', True)
        extra_fields.setdefault('is_trial', True)
        extra_fields.setdefault('is_system_admin', False)
        user.save(using=self.db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_pro', True)
        extra_fields.setdefault('is_trial', True)
        extra_fields.setdefault('is_system_admin', True)

        if extra_fields.get('is_system_admin') is not True:
            raise ValueError('Super_Admin must have is_system_admin=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(verbose_name="email address", max_length=30, unique=True)
    password = models.CharField()
    is_system_admin = models.BooleanField(default=False)
    is_pro = models.BooleanField(default=True)
    is_trial = models.BooleanField(default=True)
    refresh_token = models.CharField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = True
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["password"]

    objects = UserManager()

    def __str__(self):
        return self.email
