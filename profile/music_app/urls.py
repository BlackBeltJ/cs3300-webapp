from django.urls import path
from . import views
from .models import *

urlpatterns = [
    # path function defines a url pattern
    # ' is empty to represent based path to app
    # views.index is the function defined in views.py 
    # name='index' parameter is to dynamically create url
    # example in html ,a href="{% url 'index' %}">Home</a>
    path('', views.index, name='index'),
    
    path('login/', views.index, name='login'),
    path('logout/', views.index, name='logout'),
    
    path('artists/', views.ArtistListView.displayArtists, name='artists'),
    path('artists/<int:pk>', views.ArtistDetailView.artistDetail, name='artist-detail'),
    path('artists/<int:pk>/profile', views.ProfileDetailView.profileDetail, name='profile-detail'),
    #.as_view() is a method that returns a default view function
    path('artist/?/profile/project/<int:pk>', views.ProjectDetailView.projectDetail, name='project-detail'),
    path('artist/<int:pk>/profile/edit', views.editProfile, name='edit-profile'),
    #<uuid:pk> is a path converter that matches a UUID
    path('artist/<int:pk>/profile/create_project', views.ProjectOperations.createProject, name='create-project'),
    path('artist/?/profile/update_project/<int:pk>', views.ProjectOperations.updateProject, name='update-project'),
    path('artist/?/profile/delete_project/<int:pk>', views.ProjectOperations.deleteProject, name='delete-project'),

    path('create_artist/', views.CreationOperations.createArtistAndProfile, name='create-artist'),
    #path('register/', views.register, name='register'),
]