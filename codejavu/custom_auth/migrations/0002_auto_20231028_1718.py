# Generated by Django 4.2.5 on 2023-10-28 17:18

import logging

from django.db import migrations
import os
logger = logging.getLogger(__name__)


def generate_superuser(apps, schema_editor):
    from django.contrib.auth import get_user_model

    # env = environ.Env()
    PASSWORD = os.getenv('SYS_ADMIN_PASSWORD')
    EMAIL = os.getenv("SYS_ADMIN_EMAIL")

    user = get_user_model()

    if not user.objects.filter(email=EMAIL).exists():
        logger.info("Creating new superuser")
        admin = user.objects.create_superuser(
            email=EMAIL, password=PASSWORD
        )
        admin.save()
    else:
        logger.info("Superuser already created!")


class Migration(migrations.Migration):
    dependencies = [
        ('custom_auth', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(generate_superuser)
    ]
