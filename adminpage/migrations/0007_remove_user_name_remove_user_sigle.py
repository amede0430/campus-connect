# Generated by Django 4.2.11 on 2024-05-24 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0006_user_sigle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='sigle',
        ),
    ]
