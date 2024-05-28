from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login as auth_login ,authenticate,logout as auth_logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.core import serializers
from django.views.decorators.http import require_GET
from django.template import loader
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UniversiteForm,UserForm,FiliereForm,ClasseForm,EtudiantForm,FisrtSemestreForm,SecondSemestreForm,ReinscrireForm
from .models import Universite,User,Filiere,Classe,Etudiant,EtudiantFiliere
# Create your views here.


#vérifier si c'est un super admin
def is_superAdmin(user):
    return user.is_authenticated and user.is_superuser

#vérifier si c'est un admin d'école
def is_admin(user):
    return user.is_authenticated and not user.is_superuser

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None :
            auth_login(request,user)
            if user.is_superuser:
                return redirect('index')
            else :
                return redirect('entite')
        else :
            messages.error(request, "Identifiants incorrects")
    return render(request, 'login.html')

@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    return redirect('login')

@user_passes_test(is_superAdmin, login_url='login')
def index(request):
    if request.method == "POST":
        form = UniversiteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Ajout d'université avec succès")
            return redirect('index') 
    else:
        form = UniversiteForm()
        
    universites =  Universite.objects.all()
    forms = []
    for u in universites:
        forms.append(UniversiteForm(instance=u))

    uf = zip(universites,forms)
    
    upub = Universite.objects.filter(universite_type = 'Publique').count()
    upriv = Universite.objects.filter(universite_type = 'Privé').count()
    nbree = User.objects.filter(is_superuser=0).count()
    nbref = 0
    entites = User.objects.filter(is_superuser=0)
    for e in entites:
        nbref+=Filiere.objects.filter(entite=e).count()
    
    return render(request, 'adminpage/index.html',{'form':form,'uf':uf,'upub':upub,'upriv':upriv,'nbree':nbree,'nbref' : nbref})

@user_passes_test(is_superAdmin, login_url='login')
def update_universite(request, id):
    universite = get_object_or_404(Universite, id=id)
    if request.method == 'POST':
        form = UniversiteForm(request.POST, request.FILES, instance=universite)
        if form.is_valid():
            form.save()
            messages.success(request,"Modification d'université avec succès")
            return redirect('index')
    else:
        form = UniversiteForm(instance=universite)
    return redirect('index')

@user_passes_test(is_superAdmin, login_url='login')
def delete_universite(request, id):
    universite = get_object_or_404(Universite, id=id)
    universite.delete()
    messages.success(request,"Suppression d'université avec succès")
    return redirect("index")

@user_passes_test(is_superAdmin, login_url='login')
def details(request, id):
    u = get_object_or_404(Universite, id=id)
    
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.universite = u
            user.username =  (form.cleaned_data['sigle']).lower() +'.campus'
            user.set_password('campus')
            user.save()
            messages.success(request, "Ajout d'entité avec succès")
            return redirect('details', id = u.id)
    else:
        form = UserForm()
        
    entites = User.objects.filter(universite=u)
    nbreEntites = entites.count()

    return render(request, 'adminpage/details.html', {'u': u, 'entites': entites, 'form': form,'nbre' : nbreEntites})

@user_passes_test(is_admin, login_url='login')
def entite(request):
    user = request.user
    univ = get_object_or_404(Universite,id=user.universite_id)
    if request.method == "POST":
        form = FiliereForm(request.POST, request.FILES)
        if form.is_valid():
            filiere = form.save(commit=False)
            filiere.entite = user
            filiere.save()
            messages.success(request,"Ajout de filière avec succès")
            return redirect('entite') 
    else:
        form = FiliereForm()
        
    filieres =  Filiere.objects.filter(entite=user)
    forms = []
    for fi in filieres:
        forms.append(FiliereForm(instance=fi))

    fif = zip(filieres,forms)
    
    return render(request, 'adminpage/entite.html',{'univ':univ,'fif':fif,'form':form,'nbref':filieres.count()})

@user_passes_test(is_admin, login_url='login')
def update_filiere(request, id):
    filiere = get_object_or_404(Filiere, id=id)
    if request.method == 'POST':
        form = FiliereForm(request.POST, request.FILES, instance=filiere)
        if form.is_valid():
            form.save()
            messages.success(request,"Modification de filière avec succès")
            return redirect('entite')
    else:
        form = FiliereForm(instance=filiere)
    return redirect('entite')

@user_passes_test(is_admin, login_url='login')
def delete_filiere(request, id):
    filiere = get_object_or_404(Filiere, id=id)
    filiere.delete()
    messages.success(request,"Suppression de filière avec succès")
    return redirect("entite")

@user_passes_test(is_admin, login_url='login')
def classes(request,id):
    user = request.user
    filiere = get_object_or_404(Filiere,id=id)
    if request.method == "POST":
        form_type = request.POST.get('form_type')
        if form_type == 'classe':
            form = ClasseForm(request.POST)
            form1 = EtudiantForm()
            if form.is_valid():
                classe = form.save(commit=False)
                if classe.niveau > filiere.nbreAnnee:
                    messages.error(request,"Revoir le niveau.")
                    return redirect('classe',id=id)
                classe.filiere = filiere
                classe.save()
                messages.success(request,"Ajout d'une nouvelle année d'étude.")
                return redirect('classe',id=id)
            
        elif form_type == 'etudiant':
            form1 = EtudiantForm(request.POST,request.FILES)
            form = ClasseForm()
            if form1.is_valid():
                classe = Classe.objects.filter(filiere=filiere,niveau=1).first()
                if classe is None:
                    messages.error(request, "Créer d'abord une première année")
                    return redirect('classe', id=id)
                
                etudiant =  Etudiant.objects.filter(matricule=form1.cleaned_data['matricule']).first()
                
                if  etudiant :
                    ok = EtudiantFiliere.objects.filter(etudiant=etudiant, filiere=filiere).count()
                    if not ok :
                        EtudiantFiliere.objects.create(etudiant=etudiant, filiere=filiere, annee_academique=form1.cleaned_data['annee_academique'],classe_id=classe.id)
                        messages.success(request, "Cet étudiant appartient une autre filière et son inscription dans celle-ci est prise en compte .")
                    else :
                        messages.error(request, "Cet étudiant appartient déjà à cette filière. Plus d'inscription possible")
                    form1 = EtudiantForm()
                    return redirect('classe', id=id)
                else :
                    etudiant = form1.save(commit=False)
                    etudiant.save()
                    EtudiantFiliere.objects.create(etudiant=etudiant, filiere=filiere, annee_academique=etudiant.annee_academique,classe_id=classe.id)
                    messages.success(request, "Ajout d'un nouvel étudiant.")
                    return redirect('classe', id=id)
         
    else:
        form = ClasseForm(id=filiere.id)
        form1 = EtudiantForm()
        
    classes =  Classe.objects.filter(filiere=filiere)
    forms = []
    for c in classes:
        forms.append(ClasseForm(instance=c,id=filiere.id))

    cf = zip(classes,forms)
    univ = get_object_or_404(Universite,id=user.universite_id)
    return render(request, 'adminpage/classes.html', {'form':form,'cf':cf,'filiere':filiere,'univ':univ,'form1':form1})

@user_passes_test(is_admin, login_url='login')
def update_classe(request, id):
    classe = get_object_or_404(Classe, id=id)
    filiere = get_object_or_404(Filiere,id=classe.filiere_id)
    if request.method == 'POST':
        form = ClasseForm(request.POST,instance=classe)
        if form.is_valid():
            classe = form.save(commit=False)
            if classe.niveau > filiere.nbreAnnee:
                messages.error(request,"Revoir le niveau.")
                return redirect('classe',id=filiere.id)
            classe.filiere = filiere
            classe.save()
            messages.success(request,"Modification de la classe avec succès")
            return redirect('classe',id=filiere.id)
    else:
        form = ClasseForm(instance=classe)
    return redirect('classe',id=filiere.id)

@user_passes_test(is_admin, login_url='login')
def delete_classe(request, id):
    classe = get_object_or_404(Classe, id=id)
    filiere = get_object_or_404(Filiere,id=classe.filiere_id)
    classe.delete()
    messages.success(request,"Suppression de la classe avec succès")
    return redirect('classe',id=filiere.id)

@user_passes_test(is_admin, login_url='login')
def check(request):
    matricule = request.GET.get('matricule')
    if not matricule:
        return JsonResponse({'error': 'Matricule is required'}, status=400)
    try:
        etudiant = Etudiant.objects.get(matricule=matricule)
        etudiant_data = {
            'matricule': etudiant.matricule,
            'nom': etudiant.nom,
            'prenoms': etudiant.prenoms,
            'email': etudiant.email,
            'date_naissance': etudiant.date_naissance,
            'adresse': etudiant.adresse,
            'phone': etudiant.phone,
            'sexe': etudiant.sexe,
            'annee_academique': etudiant.annee_academique,
        }
        return JsonResponse(etudiant_data)
    except Etudiant.DoesNotExist:
        return JsonResponse({'error': 'Etudiant not found'}, status=404)

@user_passes_test(is_admin, login_url='login')
def etudiants(request,id):
    classe = get_object_or_404(Classe,id=id)
    filiere = get_object_or_404(Filiere,id=classe.filiere_id)
    sems = [classe.niveau*2-1,classe.niveau*2]
    annee_acads = EtudiantFiliere.objects.filter(filiere=filiere,niveau=classe.niveau,classe_id=id).values('annee_academique').distinct().order_by('-annee_academique')
    if annee_acads:
        current_year = annee_acads[0]['annee_academique']
        ef = EtudiantFiliere.objects.filter(filiere=filiere,niveau=classe.niveau,annee_academique=current_year,classe_id=id)
        
        etudiants = []
        for e in ef:
            etudiants.append(Etudiant.objects.filter(id=e.etudiant_id).get())
        etuAndfil = zip(etudiants,ef)
        return render(request, 'adminpage/etudiants.html',{'classe':classe,'filiere':filiere,'annee_acads':annee_acads,'etufil':etuAndfil,'sems':sems})
    
    return render(request, 'adminpage/etudiants.html',{'classe':classe,'filiere':filiere,'annee_acads':annee_acads,'etufil':zip([],[]),'sems':sems})

@user_passes_test(is_admin, login_url='login')
def saisie(request,idclasse,idetudiant):
    etudiant = get_object_or_404(Etudiant,id=idetudiant)
    classe = get_object_or_404(Classe,id=idclasse)
    filiere = get_object_or_404(Filiere,id=classe.filiere_id)
    ef = EtudiantFiliere.objects.filter(etudiant=etudiant,filiere=filiere,niveau=classe.niveau).last()
    
    if request.method == "POST":
        form_type = request.POST.get('form_type')
        if form_type == "first":
            form = FisrtSemestreForm(request.POST,instance=ef)
            if form.is_valid():
                # form.save(commit=False)
                form.save()
                return redirect('etudiants', classe.id)
            else :
                firstForm = FisrtSemestreForm(request.POST)
                secondForm = SecondSemestreForm(instance=ef)
        else:
            form = SecondSemestreForm(request.POST,instance=ef)
            if form.is_valid():
                ef = form.save(commit=False)
                ef.moy = (ef.moy_sem1 + ef.moy_sem2)/2
                if ef.credit_sem1 + ef.credit_sem2 == 60:
                    ef.decision = 1
                elif 48 <= ef.credit_sem1 + ef.credit_sem2 < 60 :
                    ef.decision = 2
                else :
                    ef.decision = 3
                ef.save()
                return redirect('etudiants', classe.id)
            else :
                firstForm = FisrtSemestreForm(instance=ef)
                secondForm = SecondSemestreForm(request.POST)
    else:
        firstForm = FisrtSemestreForm(instance=ef)
        secondForm = SecondSemestreForm(instance=ef)
    return render(request, 'adminpage/saisie.html',{'etudiant':etudiant,'classe':classe,'filiere':filiere,'ef':ef,'firstForm':firstForm,'secondForm':secondForm})

@user_passes_test(is_admin, login_url='login')
def reinscrire(request,idclasse,idetudiant):
    etudiant = get_object_or_404(Etudiant,id=idetudiant)
    classe = get_object_or_404(Classe,id=idclasse)
    filiere = get_object_or_404(Filiere,id=classe.filiere_id)
    ef = EtudiantFiliere.objects.filter(etudiant=etudiant,filiere=filiere,niveau=classe.niveau).last()
    
    if ef.decision == 1 or ef.decision == 2 :
        niveau = classe.niveau+1
    else : 
        niveau = classe.niveau
    
    if request.method == "POST":
        etuAndFil = EtudiantFiliere(etudiant=etudiant,filiere=filiere)
        form = ReinscrireForm(request.POST,instance=etuAndFil)
        if form.is_valid():
             if form.cleaned_data['annee_academique'] <= ef.annee_academique:
                 messages.error(request,'Année académique non valide')
                 return redirect('reinscrire', classe.id,etudiant.id)
             else :
                 ef.reinscrit = True
                 ef.save()
                 etuAndFil = form.save(commit=False)
                 etuAndFil.niveau = (get_object_or_404(Classe,id=etuAndFil.classe_id)).niveau
                 etuAndFil.save()
             return redirect('etudiants', classe.id)
        else :
            form = ReinscrireForm(request.POST,id=filiere.id,niv=niveau)
    else :
        form = ReinscrireForm(id=filiere.id,niv=niveau)
    return render(request, 'adminpage/reinscrire.html',{'etudiant':etudiant,'classe':classe,'filiere':filiere,'ef':ef,'form':form})

@user_passes_test(is_admin, login_url='login')
def show(request):
    annee_academique = request.GET.get('annee_academique')
    id = request.GET.get('classe_id')
    
    if not annee_academique:
        return JsonResponse({'error': 'Year and Classe_id is required'}, status=400)
    
    try:
        classe = Classe.objects.filter(id=id).first()
        print(classe.niveau)
        filiere = Filiere.objects.filter(id=classe.filiere_id).first()
        ef = EtudiantFiliere.objects.filter(filiere=filiere, niveau=classe.niveau, annee_academique=annee_academique, classe_id=id)
        
        etudiants = []
        for e in ef:
            etudiant = Etudiant.objects.filter(id=e.etudiant_id).first()
            etudiants.append({
                'id': etudiant.id,
                'nom': etudiant.nom,
                'prenoms': etudiant.prenoms,
                'matricule': etudiant.matricule,
            })
        
        etudiants_data = {
            'ef': serializers.serialize('json', ef),
            'etudiants': etudiants
        }
        return JsonResponse(etudiants_data)
    
    except Etudiant.DoesNotExist:
        return JsonResponse({'error': 'Etudiants not found'}, status=404)

@user_passes_test(is_admin, login_url='login')
def etudiant(request,id):
    etudiant = Etudiant.objects.filter(id=id).first()
    fil =  EtudiantFiliere.objects.filter(etudiant=etudiant).values('filiere_id').distinct()
    ids = []
    for filiere in fil:
        filiere_id = filiere['filiere_id']
        filiere_name = Filiere.objects.get(id=filiere_id).id
        ids.append(filiere_name)
    print(ids)
    
    cursus = []
    for i in ids:
        filiere = Filiere.objects.get(id=i)
        entite = User.objects.get(id=filiere.entite_id)
        univ = Universite.objects.get(id=entite.universite_id)
        efs = EtudiantFiliere.objects.filter(etudiant=etudiant, filiere=filiere)
        classes = [Classe.objects.get(id=ef.classe_id) for ef in efs]
        efc = zip(efs, classes)
        c = {'filiere': filiere, 'entite': entite, 'univ': univ, 'efc': efc}
        cursus.append(c)
    # print(cursus)
    return render(request, 'adminpage/etudiant.html',{'etudiant':etudiant,'cursus':cursus})