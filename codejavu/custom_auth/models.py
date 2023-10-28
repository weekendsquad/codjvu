from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have a valid email address")
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.email = email
        user.is_pro = True
        user.is_active = True
        user.is_trial = True
        user.is_system_admin = False
        user.save(using=self.db)
        return user


class User(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(verbose_name="email address", max_length=30, unique=True)
    password = models.CharField()
    is_system_admin = models.BooleanField(default=False)
    is_pro = models.BooleanField(default=False)
    is_trial = models.BooleanField(default=False)
    refresh_token = models.CharField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = True
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["password"]

    objects = UserManager()

    def __str__(self):
        return self.email
