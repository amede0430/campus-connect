# Generated by Django 4.2.11 on 2024-05-26 06:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0018_etudiant_profil'),
    ]

    operations = [
        migrations.RenameField(
            model_name='etudiantfiliere',
            old_name='credit_sem',
            new_name='credit_sem2',
        ),
    ]
