# Generated by Django 4.2.5 on 2024-02-09 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippet', '0011_url_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='user_id',
            new_name='user',
        ),
    ]
