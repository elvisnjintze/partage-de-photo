from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from blog.models import PhotoProfil
class LoginForms(forms.Form):
    username = forms.CharField(max_length=63, label='Nom utilisateur')
    password = forms.CharField(max_length=63, label='Mot de passe', widget=forms.PasswordInput)
#cette classe permet l'inscription d'un nouveau utilisateur
#nous utilisons la superclasse UserCreationForm pour le formulaire qui
#hérite tout aussi de la classe ModelForm
#et nous spécifions dans le champ fields toutes les champs que nous aimerions
# que le nouveau utilisateur renseigne
class SingupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username','first_name','last_name','email','role')

class UploadProfilPhotoForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('profile_photo')
