from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
# Create your views here.
from . import forms
from django.conf import settings

def login_page(request):
    form = forms.LoginForms()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForms(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                message = 'connection échouée mon patron identifiant invalide'

    return render(request,'authentication/login.html', {'form':form,'message':message})

def logout_user(request):
    logout(request)
    return redirect('login')
# création d'une connection basée sur la classe
# au de celui basée sur la fonction(login_page)
#il se pose un pb avec l'attribut cleaned_data que j'ai
# du remplacer par request.POST

class LoginPageView(View):
    template_name = 'authentication/login.html'
    form_class = forms.LoginForms
    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, {'form':form, 'message':message})
    def post(self, request):
        form = form_ = self.form_class(request.POST)
        if form.is_valid:
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request,user)
                return redirect('home')
        message = 'identifiant invalide'
        return render(request, self.template_name, {'form':form,'message':message})

#création de la vue qui se chargera de l'inscriptioln
def signup(request):
    form = forms.SingupForm()
    if request.method=='POST':
        form = forms.SingupForm(request.POST)
        if form.is_valid():
            user = form.save()
            #loguer l'user
            login(request,user)
            return redirect(settings.LOGIN_URL)
            #return redirect('home')
    return render(request,'authentication/signup.html', {'form':form})


def upload_photo_profil(request):
    form = forms.UploadProfilPhotoForm(instance=request.user)
    if request.method=='POST':
        form = forms.UploadProfilPhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid:
            form.save()
            return redirect('home')
    return render(request, 'authentication/uploadphotoprofil.html', {'form':form})

