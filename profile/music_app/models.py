from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):  
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False, blank = False)
    about = models.TextField("About (Optional)", blank=True)
    contact_email = models.EmailField("Contact Email", max_length=50)
   # student = models.OneToOneField(Student, null=True, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.title

    #Returns the URL to access a particular instance of MyModelName.
    #if you define this method then Django will automatically
    # add a "View on Site" button to the model's record editing screens in the Admin site
    def get_absolute_url(self):
        return reverse('profile-detail', args=[str(self.id)])
    
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
    profile = models.OneToOneField(Profile, null=True, on_delete=models.CASCADE, unique=True) 
    
    def __str__(self):
        return self.name

    #Returns the URL to access a particular instance of MyModelName.
    #if you define this method then Django will automatically
    # add a "View on Site" button to the model's record editing screens in the Admin site
    def get_absolute_url(self):
        return reverse('artist-detail', args=[str(self.id)])

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField("Project Description", blank = False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

    #Returns the URL to access a particular instance of MyModelName.
    #if you define this method then Django will automatically
    # add a "View on Site" button to the model's record editing screens in the Admin site
    def get_absolute_url(self):
        return reverse('project-detail', args=[str(self.id)])

#class User(models.Model):
#   user_id = models.CharField(max_length=200)