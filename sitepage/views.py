from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import *
# Create your views here.

def index(request):
    univs_pub = Universite.objects.filter(universite_type="Publique")
    univs_priv = Universite.objects.filter(universite_type="Privé")
    entites = User.objects.filter(is_superuser = 0)
    filieres = Filiere.objects.all()
    return render(request, 'sitepage/index.html',{'univs_pub':univs_pub,'univs_priv':univs_priv,'entites':entites,'filieres':filieres})
