# Generated by Django 4.2.11 on 2024-05-23 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0005_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sigle',
            field=models.CharField(blank=True, max_length=150, verbose_name='first_name'),
        ),
    ]
