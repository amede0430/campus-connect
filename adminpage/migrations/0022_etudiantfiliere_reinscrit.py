# Generated by Django 4.2.11 on 2024-05-27 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0021_alter_etudiantfiliere_credit_sem1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='etudiantfiliere',
            name='reinscrit',
            field=models.BooleanField(default=0),
        ),
    ]
