from django.db import models
from custom_auth.models import User


class Language(models.Model):
    id = models.BigAutoField(primary_key=True)
    language = models.CharField(max_length=30, unique=True)


class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=30, unique=True)
