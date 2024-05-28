from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.

class Universite(models.Model):
    name = models.CharField(max_length=100)
    sigle = models.CharField(max_length=10,null=True)
    location = models.CharField(null=True, max_length=100)  
    universite_type = models.CharField(null=False,max_length=50)  
    email = models.EmailField(null=False, max_length=50) 
    phone = models.CharField(null=False, max_length=50)
    site = models.CharField(null=True, max_length=50)
    logo = models.ImageField(upload_to='u-logos/')



class User(AbstractUser):
    universite = models.ForeignKey(Universite, on_delete=models.CASCADE, null=True) 
    description = models.CharField(null=True, max_length=100)  
    location = models.CharField(null=True, max_length=100)
    ecole_type = models.CharField(null=True,max_length=50)  
    email = models.EmailField(null=True, max_length=50) 
    phone = models.CharField(null=True, max_length=50)
    site = models.CharField(null=True, max_length=50)
    logo = models.ImageField(upload_to='e-logos/')
    name = models.CharField(max_length=150, blank=True, verbose_name="Name")
    sigle = models.CharField(max_length=150, blank=True, verbose_name="Sigle")
    
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Filiere(models.Model):
    name = models.CharField(max_length=150, blank=True)
    sigle = models.CharField(max_length=150, blank=True)
    entite = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    diplome = models.CharField(max_length=150, blank=True)
    nbreAnnee = models.IntegerField()
    description = models.CharField(null=True, max_length=100)  
    location = models.CharField(null=True, max_length=100)
    email = models.EmailField(null=True, max_length=50) 
    phone = models.CharField(null=True, max_length=50)
    site = models.CharField(null=True, max_length=50)
    logo = models.ImageField(upload_to='f-logos/')

class Classe(models.Model):
    name = models.CharField(max_length=150, blank=True)
    sigle = models.CharField(max_length=150, blank=True)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, null=True)
    option = models.CharField(max_length=150, blank=True, null=True)
    option_sigle = models.CharField(max_length=150, blank=True, null=True)
    niveau = models.IntegerField(default=1)
    description = models.CharField(null=True, max_length=100) 
    
class Etudiant(models.Model):
    matricule = models.CharField(max_length=150, blank=True)
    nom = models.CharField(max_length=150, blank=True)
    prenoms = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=150, blank=True)
    filieres = models.ManyToManyField(Filiere, through='EtudiantFiliere')
    date_naissance = models.DateField(null=False)
    adresse = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=15, null=True)
    sexe = models.CharField(max_length=1, null=True)
    annee_academique = models.CharField(max_length=9,blank=True)
    profil = models.ImageField(upload_to='et-logos/')

class Decision(models.IntegerChoices):
    ATTENTE = 0,
    ADMIS = 1,
    ENJAMBE = 2,
    ECHOUE = 3,

class EtudiantFiliere(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    classe_id = models.BigIntegerField(default=5)
    annee_academique = models.CharField(max_length=9,blank=True)
    niveau = models.IntegerField(default=1)
    moy_sem1 = models.FloatField(default=0,validators=[MaxValueValidator(100),MinValueValidator(0)])
    credit_sem1 = models.IntegerField(default=0,validators=[MaxValueValidator(30),MinValueValidator(0)])
    moy_sem2 = models.FloatField(default=0,validators=[MaxValueValidator(100),MinValueValidator(0)])
    credit_sem2 = models.IntegerField(default=0,validators=[MaxValueValidator(30),MinValueValidator(0)])
    moy = models.FloatField(default=0)
    decision = models.IntegerField(choices=Decision.choices, default=Decision.ATTENTE)
    reinscrit = models.BooleanField(default=0)
    