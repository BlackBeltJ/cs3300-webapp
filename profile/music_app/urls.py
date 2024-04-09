from django.urls import path, include
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
    #path('login/', views.ArtistAuth.login, name='login'),
    #path('/accounts/logout/', views.ArtistAuth.logged_outPage, name='logout'),
    
    # artist operations (display, create, edit, delete, etc)
    path('artists/', views.ArtistOperations.displayArtists, name='artists'),
    #path('artists/<int:pk>', views.ArtistOperations.artistDetail, name='artist-detail'),
    path('artists/<int:pk>', views.ArtistOperations.userPage, name='artist-detail'),
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

    # artist accounts
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.ArtistAuth.registerPage, name='register-page'),
    path('accounts/login/', views.ArtistAuth.loginPage, name='login-page'),
    path('accounts/logout/', views.ArtistAuth.logoutPage, name='logout-page'),
    #the following include automatically maps the following urls
    #accounts/ login/ [name='login']
    #accounts/ logout/ [name='logout']
    #accounts/ password_change/ [name='password_change']
    #accounts/ password_change/done/ [name='password_change_done']
    #accounts/ password_reset/ [name='password_reset']
    #accounts/ password_reset/done/ [name='password_reset_done']
    #accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
    #accounts/ reset/done/ [name='password_reset_complete']
    
    
]