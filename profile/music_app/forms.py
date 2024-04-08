from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import Project, Profile, Artist

  
class EditProfileForm(ModelForm): #forms.Form 
    class Meta:
        model = Profile
        fields = ['title', 'is_public', 'about', 'contact_email']
    
        #title = forms.CharField(max_length=200, required=True)
        #is_active = forms.BooleanField(required=False)
        #about = forms.CharField(widget=forms.Textarea, required=True)
        #contact_email = forms.EmailField(required=True)

class ArtistForm(ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'email', 'genre', 'instrument']

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']

# class UserCreationForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
#         widgets = {
#             'password1': forms.PasswordInput(),
#             'password2': forms.PasswordInput()
#         }
    
#     def save(self, commit=True):
#         user = super(UserCreationForm, self).save(commit=False)
#         user.email = self.cleaned_data['email']
#         if commit:
#             user.save()
#         return user