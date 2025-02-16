# Generated by Django 4.2.11 on 2024-05-25 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0012_remove_classe_entite_classe_filiere_classe_niveau_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Etudiant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricule', models.CharField(blank=True, max_length=150, unique=True)),
                ('nom', models.CharField(blank=True, max_length=150)),
                ('prenoms', models.CharField(blank=True, max_length=150)),
                ('email', models.EmailField(blank=True, max_length=150)),
                ('date_naissance', models.DateField()),
                ('adresse', models.CharField(max_length=255, null=True)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('sexe', models.CharField(max_length=1, null=True)),
                ('date_inscription', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='EtudiantFiliere',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etudiant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminpage.etudiant')),
                ('filiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminpage.filiere')),
            ],
        ),
        migrations.AddField(
            model_name='etudiant',
            name='filieres',
            field=models.ManyToManyField(through='adminpage.EtudiantFiliere', to='adminpage.filiere'),
        ),
    ]
