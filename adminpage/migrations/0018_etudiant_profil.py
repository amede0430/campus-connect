# Generated by Django 4.2.11 on 2024-05-26 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0017_alter_etudiant_matricule'),
    ]

    operations = [
        migrations.AddField(
            model_name='etudiant',
            name='profil',
            field=models.ImageField(default='et-logos/profil.1.jpg', upload_to='et-logos/'),
            preserve_default=False,
        ),
    ]
