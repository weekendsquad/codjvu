from django.db import models


class Language(models.Model):
    id = models.BigAutoField(primary_key=True)
    language = models.CharField(max_length=30, unique=True)
