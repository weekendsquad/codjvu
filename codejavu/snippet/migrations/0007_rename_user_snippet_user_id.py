# Generated by Django 4.2.5 on 2024-02-04 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippet', '0006_remove_snippet_uuid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='snippet',
            old_name='user',
            new_name='user_id',
        ),
    ]
