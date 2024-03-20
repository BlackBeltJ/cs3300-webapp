from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse

# Create your models here.
class Portfolio(models.Model):  
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False, blank = False)
    about = models.TextField("About (Optional)", blank=True)
    contact_email = models.CharField("Contact Email", max_length=200)
   # student = models.OneToOneField(Student, null=True, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.title

    #Returns the URL to access a particular instance of MyModelName.
    #if you define this method then Django will automatically
    # add a "View on Site" button to the model's record editing screens in the Admin site
    def get_absolute_url(self):
        return reverse('portfolio-detail', args=[str(self.id)])

    
class Student(models.Model):
#List of choices for major value in database, human readable name
    MAJOR = (
    ('CSCI-BS', 'BS in Computer Science'),
    ('CPEN-BS', 'BS in Computer Engineering'),
    ('BIGD-BI', 'BI in Game Design and Development'),
    ('BICS-BI', 'BI in Computer Science'),
    ('BISC-BI', 'BI in Computer Security'),
    ('CSCI-BA', 'BA in Computer Science'),
    ('DASE-BS', 'BS in Data Analytics and Systems Engineering')
    )
    name = models.CharField(max_length=200)
    email = models.CharField("UCCS Email", max_length=200)
    major = models.CharField(max_length=200, choices=MAJOR, blank = False)
    portfolio = models.OneToOneField(Portfolio, null=True, on_delete=models.CASCADE, unique=True) 
    
    def __str__(self):
        return self.name

    #Returns the URL to access a particular instance of MyModelName.
    #if you define this method then Django will automatically
    # add a "View on Site" button to the model's record editing screens in the Admin site
    def get_absolute_url(self):
        return reverse('student-detail', args=[str(self.id)])


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField("Project Description", blank = False)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

    #Returns the URL to access a particular instance of MyModelName.
    #if you define this method then Django will automatically
    # add a "View on Site" button to the model's record editing screens in the Admin site
    def get_absolute_url(self):
        return reverse('project-detail', args=[str(self.id)])

#class User(models.Model):
#   user_id = models.CharField(max_length=200)