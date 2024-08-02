from django import forms
from . import models
from django.contrib.auth import get_user_model #ceci permet d'avoir l'instance de l'utilisateur connecté
from authentication.models import User
class PhotoForms(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image','caption']

class BlogForms(forms.ModelForm):
    contributors = forms.ModelMultipleChoiceField(
        queryset= User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = models.Blog
        fields = ['title', 'content','contributors']

class BlogForm(forms.ModelForm):
    """ceci doit permettre la modification d'un blog"""
    edit_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = models.Blog
        fields =['title', 'content',]

class DeleteBlogForm(forms.Form):
    """cettte classe doit permettre la sippression d'un blog"""
    delete_blog = forms.BooleanField(widget= forms.HiddenInput, initial=True)

class FollowUserForm(forms.ModelForm):
    class Meta:
        #model = get_user_model()
        model = User()
        fields = ['follow']


