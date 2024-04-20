from django.urls import path, include
from . import views
from .models import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path function defines a url pattern
    # ' is empty to represent based path to app
    # views.index is the function defined in views.py 
    # name='index' parameter is to dynamically create url
    # example in html ,a href="{% url 'index' %}">Home</a>
    #.as_view() is a method that returns a default view function
    #<uuid:pk> is a path converter that matches a UUID
    path('', views.index, name='index'), # default view, home page
    # register
    path('register/', views.ArtistAuth.registerPage, name='register-page'),
    # artist operations (display, create, edit, delete, etc)
    path('artists/', views.ArtistOperations.displayArtists, name='artists'),
    # had to create another path for artist-detail-from-base because I can't access the artist from base_template
    # I can only access the user from base_template.html so I made a new function that takes the user.id as user_pk and gets the artist from there
    path('user/<int:user_pk>', views.ArtistOperations.artistDetailFromBase, name='artist-detail-from-base'),
    path('artists/<int:pk>', views.ArtistOperations.artistDetail, name='artist-detail'),
    #path('accounts/create_artist/', views.ArtistOperations.createArtistAndProfile, name='create-artist'),
    path('delete_artist/<int:pk>', views.ArtistOperations.deleteArtistAndProfile, name='delete-artist'),
    # profile operations (display, create, edit, delete, etc)
    path('artists/<int:pk>/profile', views.ProfileOperations.profileDetail, name='profile-detail'),
    path('artist/<int:pk>/profile/edit', views.ProfileOperations.editProfile, name='edit-profile'),
    # post operations (display, create, edit, delete, etc)
    path('artist/?/profile/post/<int:pk>', views.PostOperations.postDetail, name='post-detail'),
    path('artist/<int:pk>/profile/create_post', views.PostOperations.createPost, name='create-post'),
    path('artist/<int:pk>/profile/update_post/<int:post_pk>', views.PostOperations.updatePost, name='update-post'),
    path('artist/<int:pk>/profile/delete_post/<int:post_pk>', views.PostOperations.deletePost, name='delete-post'),
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

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)