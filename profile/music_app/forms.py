from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import Post, Profile, Artist #, User
from django.core.exceptions import ValidationError
import os
  
class ProfileForm(ModelForm): #forms.Form 
    class Meta:
        model = Profile
        fields = ['title', 'is_public', 'about', 'contact_email']

class ArtistForm(ModelForm):
    class Meta:
        model = Artist
        fields = '__all__'
        exclude = ['user', 'profile']
        
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['profile']
        
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
