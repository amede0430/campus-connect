from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    
    path('', views.index, name='index'),
    path('update/<int:id>/', views.update_universite, name='update_universite'),
    path('delete/<int:id>/', views.delete_universite, name='delete_universite'), 
    path('u-details/<int:id>/', views.details, name='details'),
    
    path('entite', views.entite, name='entite'),
    path('f-update/<int:id>/', views.update_filiere, name='update_filiere'),
    path('f-delete/<int:id>/', views.delete_filiere, name='delete_filiere'), 
    
    path('classes/<int:id>/', views.classes, name='classe'),
    path('c-update/<int:id>/', views.update_classe, name='update_classe'),
    path('c-delete/<int:id>/', views.delete_classe, name='delete_classe'),
    path('check-etudiant/', views.check, name='check'),
    
    
    path('etudiants/<int:id>', views.etudiants, name='etudiants'),
    path('show-etudiants/', views.show, name='show'),
    path('saisie/<int:idclasse>/<int:idetudiant>', views.saisie, name='saisie'),
    path('reinscrire/<int:idclasse>/<int:idetudiant>', views.reinscrire, name='reinscrire'),
    
    path('etudiant/<int:id>', views.etudiant, name='etudiant'),
]