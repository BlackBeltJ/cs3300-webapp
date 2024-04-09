from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import Project, Profile, Artist

  
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
        
class CreateArtistForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        # widgets = {
        #     'password1': forms.PasswordInput(),
        #     'password2': forms.PasswordInput()
        # }
    
    # def save(self, commit=True):
    #     user = super(UserCreationForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #     return user
    
#   class Meta:
#       model = User
#       fields = ['username', 'email', 'password1', 'password2']
#       widgets = {
#           'password1': forms.PasswordInput(),
#           'password2': forms.PasswordInput()
#       }

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']
