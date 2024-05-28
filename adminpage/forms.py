# adminpage/forms.py
from django.shortcuts import get_object_or_404
from django import forms
from .models import Universite,User,Filiere,Classe,Etudiant,EtudiantFiliere

class UniversiteForm(forms.ModelForm):
    class Meta:
        model = Universite
        fields = ['name', 'sigle', 'location', 'universite_type', 'email', 'phone', 'site', 'logo']
        types = ['Publique','Privé']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Enter a name.', 'required': True}),
            'sigle': forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Enter a sigle.', 'required': True}),
            'location': forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Enter a city.', 'required': True}),
            'universite_type': forms.Select(attrs={'class': 'form-control'}, choices=[(type, type) for type in types]),
            'email': forms.EmailInput(attrs={'class': 'form-control ', 'placeholder': 'example@gmail.com.', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control ', 'placeholder': '+229 52747455', 'required': True}),
            'site': forms.URLInput(attrs={'class': 'form-control ', 'placeholder': 'https:/uac.bj', 'required': False}),
            'logo': forms.FileInput(attrs={'class': 'form-control ', 'accept': 'image/*' , 'required': False}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'name', 'sigle', 'email','location', 'ecole_type', 'phone', 'site', 'description', 'logo'
        ]
        types = ["École", "Faculté"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'sigle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sigle'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description','rows':'2'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'ecole_type': forms.Select(attrs={'class': 'form-control'}, choices=[(type, type) for type in types]),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'site': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Website'}),
            'logo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*', 'required': False}),
        }

class FiliereForm(forms.ModelForm):
    class Meta:
        model = Filiere
        fields = [
            'name', 'sigle','diplome','nbreAnnee','description', 'location', 'email', 'phone', 'site', 'logo'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a name.', 'required': True}),
            'sigle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a sigle.', 'required': True}),
            'diplome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a diplome name.', 'required': True}),
            'nbreAnnee': forms.Select(attrs={'class': 'form-control'}, choices=[(nbre, nbre) for nbre in [3,5]]),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter a description.', 'required': True,'rows':'2'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a location.', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@gmail.com.', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+229 52747455', 'required': True}),
            'site': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://uac.bj'}),
            'logo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

class ClasseForm(forms.ModelForm):
    def __init__(self, *args, id=None, **kwargs):
        super(ClasseForm, self).__init__(*args, **kwargs)
        self.id = id
        if self.id is not None:
            filiere = get_object_or_404(Filiere, id=self.id)
            n = filiere.nbreAnnee
            self.fields['niveau'].widget.choices = [(nbre, nbre) for nbre in range(1, n+1)]

    class Meta:
        model = Classe
        fields = [
            'name', 'sigle', 'option', 'option_sigle', 'niveau', 'description'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a name.', 'required': True}),
            'sigle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a sigle.', 'required': True}),
            'option': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a diplome name.', 'required': True}),
            'option_sigle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a option sigle.', 'required': True}),
            'niveau': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter a description.', 'required': True, 'rows': '2'}),
        }

class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = [
            'matricule',
            'nom',
            'prenoms',
            'email',
            'date_naissance',
            'adresse',
            'phone',
            'sexe',
            'annee_academique',
            'profil'
        ]
        widgets = {
            'matricule': forms.TextInput(attrs={'class': 'form-control', 'id':'matricule' , 'placeholder': 'Enter a matricule.', 'required': True}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'id':'nom', 'placeholder': 'Enter the last name.', 'required': True}),
            'prenoms': forms.TextInput(attrs={'class': 'form-control', 'id':'prenoms', 'placeholder': 'Enter the first names.', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id':'email', 'placeholder': 'Enter an email.', 'required': True}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'id':'date_naissance', 'type': 'date', 'required': True}),
            'adresse': forms.TextInput(attrs={'class': 'form-control', 'id':'adresse', 'placeholder': 'Enter the address.', 'required': False}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'id':'phone', 'placeholder': 'Enter a phone number.', 'required': False}),
            'sexe': forms.TextInput(attrs={'class': 'form-control', 'id':'sexe', 'placeholder': 'Enter the gender (M/F).', 'required': False}),
            'annee_academique': forms.TextInput(attrs={'class': 'form-control','id':'annee_academique', 'placeholder':'2022-2023','maxlength': '9', 'minlength': '9', 'required': False}),
            'profil': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}), 
        }

class FisrtSemestreForm(forms.ModelForm):
    class Meta:
        model = EtudiantFiliere
        fields = [
            'moy_sem1',
            'credit_sem1',
        ]
        widgets = {
            'moy_sem1': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Moyenne', 'required': True}),
            'credit_sem1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Credit', 'required': True})
        }
        
class SecondSemestreForm(forms.ModelForm):
    class Meta:
        model = EtudiantFiliere
        fields = [
            'moy_sem2',
            'credit_sem2',
        ]
        widgets = {
            'moy_sem2': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Moyenne', 'required': True}),
            'credit_sem2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Credit', 'required': True})
        }

class ReinscrireForm(forms.ModelForm):
    def __init__(self, *args, id=None, niv=None, **kwargs):
        super(ReinscrireForm, self).__init__(*args, **kwargs)
        self.id = id
        self.niv = niv
        if self.id is not None and self.niv is not None:
            filiere = get_object_or_404(Filiere, id=self.id)
            classes = Classe.objects.filter(filiere=filiere, niveau=niv)
            sigles = []
            for c in classes:
                sigles.append((c.id, c.option_sigle))
            self.fields['classe_id'].widget.choices = sigles
    class Meta:
        model = EtudiantFiliere
        fields = [
            'annee_academique',
            'classe_id',
        ]
        widgets = {
            'annee_academique': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': '2022-2023', 'required': True}),
            'classe_id': forms.Select(attrs={'class': 'form-control'}),
        }