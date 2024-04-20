from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import os 

# Create your models here.
class Profile(models.Model):  
    title = models.CharField(max_length=200)
    is_public = models.BooleanField(default=False, blank = False)
    about = models.TextField("About (Optional)", blank=True)
    contact_email = models.EmailField("Contact Email", max_length=50)
    
    def __str__(self):
        return self.title

    #Returns the URL to access a particular instance of MyModelName.
    #if you define this method then Django will automatically
    # add a "View on Site" button to the model's record editing screens in the Admin site
    def get_absolute_url(self):
        artist = Artist.objects.get(profile=self)
        return reverse('profile-detail', args=[str(artist.id)])
    
class Artist(models.Model):
#List of choices for major value in database, human readable name
    GENRE = (
    ('Rock', 'Rock'),
    ('Pop', 'Pop'),
    ('Christian/Worship', 'Christian/Worship'),
    ('Classical', 'Classical'),
    ('Indie', 'Indie'),
    ('Jazz', 'Jazz'),
    ('Instrumental', 'Instrumental')
    )
    name = models.CharField(max_length=200)
    email = models.EmailField("artist email", max_length=50)
    genre = models.CharField(max_length=200, choices=GENRE, blank = False)
    instrument = models.CharField(max_length=200, blank = False)
    profile = models.OneToOneField(Profile, null=True, on_delete=models.CASCADE, unique=True, blank=True) 
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.profile = Profile.objects.create(title=(f"{self.name}'s Profile"), about = (f"This is a new profile for {self.name}"), is_public=True, contact_email=self.email)
        return super(Artist, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        obj = Profile.objects.select_related('profile' == self)
        obj.delete()
        self.profile.delete()
        return super(Artist, self).delete(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    #Returns the URL to access a particular instance of MyModelName.
    #if you define this method then Django will automatically
    # add a "View on Site" button to the model's record editing screens in the Admin site
    def get_absolute_url(self):
        return reverse('artist-detail', args=[str(self.id)])

class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField("Post Description", blank = False)
    mp3_file = models.FileField(upload_to='audio/mp3/', blank=True, default = 'audio/mp3/default_audio.mp3')#null=True
    mp4_file = models.FileField(upload_to='video/mp4/', blank=True, default = 'video/mp4/default_video.mp4')#null=True
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

    #Returns the URL to access a particular instance of MyModelName.
    #if you define this method then Django will automatically
    # add a "View on Site" button to the model's record editing screens in the Admin site
    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])
    
    def get_base_mp3_filename(self):
        return os.path.basename(self.mp3_file.name)
    
    def get_base_mp4_filename(self):
        return os.path.basename(self.mp4_file.name)

# class User(models.Model):
#     username = models.CharField(max_length=200)
#     # email = models.EmailField("user's email", max_length=50)
#     # password1 = models.CharField("password", max_length=200, default="change this")
#     # password2 = models.CharField("confirm password", max_length=200, default="change this")
#     groups = models.ManyToManyField(Group, related_name='users', related_query_name='user')
#     artist = models.OneToOneField(Artist, null=True, on_delete=models.CASCADE, unique=True) 
    
#     def save(self, *args, **kwargs):
#         self.artist = Artist.objects.create(title=(f"New Profile"), about = (f"This is a new profile"), email=self.email)
#         return super(Artist, self).save(*args, **kwargs)
    
#     def delete(self, *args, **kwargs):
#         obj = Profile.objects.select_related('profile' == self)
#         obj.delete()
#         self.artist.delete()
#         return super(Artist, self).delete(*args, **kwargs)
    
#     def __str__(self):
#         return self.username