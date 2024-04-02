from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import Project, Profile, Artist

  
class EditProfileForm(ModelForm): #forms.Form 
    class Meta:
        model = Profile
        fields = ['title', 'is_active', 'about', 'contact_email']
    
        #title = forms.CharField(max_length=200, required=True)
        #is_active = forms.BooleanField(required=False)
        #about = forms.CharField(widget=forms.Textarea, required=True)
        #contact_email = forms.EmailField(required=True)

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']
