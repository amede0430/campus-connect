# Generated by Django 4.2.11 on 2024-05-25 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0009_filiere'),
    ]

    operations = [
        migrations.AddField(
            model_name='filiere',
            name='diplome',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
