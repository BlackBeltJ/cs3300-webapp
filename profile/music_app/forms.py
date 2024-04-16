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
        #fields = ['name', 'email', 'genre', 'instrument']
        exclude = ['user', 'profile']
        
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['profile']
        # widgets = {
        #     'mp3_file': forms.FileInput(attrs={'id': 'mp3_file_id'}), # 'audio/mp3
        # }
        
    # def clean_audio_file(self):
    #     file = self.cleaned_data.get('audio_file',False)
    #     if file:
    #         if file._size > 4*1024*1024:
    #            raise ValidationError("Audio file too large ( > 4mb )")
    #         if not file.content-type in ["audio/mp3"]:
    #            raise ValidationError("Content-Type is not mpeg")
    #         if not os.path.splitext(file.name)[1] in [".mp3"]:
    #            raise ValidationError("Doesn't have proper extension")
    #         # Here we need to now to read the file and see if it's actually 
    #         # a valid audio file. I don't know what the best library is to 
    #         # to do this
    #         # if not some_lib.is_audio(file.content):
    #         #       raise ValidationError("Not a valid audio file")
    #         return file
    #     else:
    #         raise ValidationError("Couldn't read uploaded file")
    
        
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
