from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import Project, Profile, Artist #, User

  
class ProfileForm(ModelForm): #forms.Form 
    class Meta:
        model = Profile
        fields = ['title', 'is_public', 'about', 'contact_email']

class ArtistForm(ModelForm):
    class Meta:
        model = Artist
        fields = '__all__'
        #fields = ['name', 'email', 'genre', 'instrument']
        exclude = ['user', 'profile']
        
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['profile']
        
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
