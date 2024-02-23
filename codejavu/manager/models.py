from django.db import models


class Setting(models.Model):
    id = models.BigAutoField(primary_key=True)
    key = models.CharField(max_length=30, unique=True)
    value = models.CharField(max_length=10, unique=True)

