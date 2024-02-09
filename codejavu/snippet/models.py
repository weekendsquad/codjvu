import uuid as uuid
from django.db import models
from custom_auth.models import User


class Language(models.Model):
    id = models.BigAutoField(primary_key=True)
    language = models.CharField(max_length=30, unique=True)


class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=30, unique=True)


class Snippet(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    snippet = models.TextField()
    language = models.ForeignKey(Language, null=True, on_delete=models.SET_NULL)


class Url(models.Model):
    id = models.BigAutoField(primary_key=True)
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()


class SnippetTag(models.Model):
    id = models.BigAutoField(primary_key=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE)
