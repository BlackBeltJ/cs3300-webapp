from django.urls import path
from . import views
from .models import *

urlpatterns = [
    # path function defines a url pattern
    # ' is empty to represent based path to app
    # views.index is the function defined in views.py 
    # name='index' parameter is to dynamically create url
    # example in html ,a href="{% url 'index' %}">Home</a>
    #.as_view() is a method that returns a default view function
    #<uuid:pk> is a path converter that matches a UUID
    path('', views.index, name='index'), # default view, home page
    
    # login and logout
    path('login/', views.index, name='login'),
    path('logout/', views.index, name='logout'),
    
    # artist operations (display, create, edit, delete, etc)
    path('artists/', views.ArtistOperations.displayArtists, name='artists'),
    path('artists/<int:pk>', views.ArtistOperations.artistDetail, name='artist-detail'),
    path('create_artist/', views.ArtistOperations.createArtistAndProfile, name='create-artist'),
    path('delete_artist/<int:pk>', views.ArtistOperations.deleteArtistAndProfile, name='delete-artist'),
    
    # profile operations (display, create, edit, delete, etc)
    path('artists/<int:pk>/profile', views.ProfileOperations.profileDetail, name='profile-detail'),
    path('artist/<int:pk>/profile/edit', views.ProfileOperations.editProfile, name='edit-profile'),
    
    # project operations (display, create, edit, delete, etc)
    path('artist/?/profile/project/<int:pk>', views.ProjectOperations.projectDetail, name='project-detail'),
    path('artist/<int:pk>/profile/create_project', views.ProjectOperations.createProject, name='create-project'),
    path('artist/?/profile/update_project/<int:pk>', views.ProjectOperations.updateProject, name='update-project'),
    path('artist/?/profile/delete_project/<int:pk>', views.ProjectOperations.deleteProject, name='delete-project'),

    #path('register/', views.register, name='register'),
]