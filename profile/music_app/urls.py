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
    # path('', views.index, name='login'),
    # path('', views.index, name='logout'),
    path('students/', views.StudentListView.displayStudents, name='students'),
    # path('student/<int:pk>', views.StudentDetailView.studentDetail, name='student-detail'),
    # path('student/<int:pk>/profile', views.ProfileDetailView.profileDetail, name='profile-detail'),
    # #.as_view() is a method that returns a default view function
    # path('student/?/profile/project/<int:pk>', views.ProjectDetailView.projectDetail, name='project-detail'),
    # path('student/<int:pk>/profile/edit', views.editProfile, name='edit-profile'),
    # #<uuid:pk> is a path converter that matches a UUID
    # path('student/<int:pk>/profile/create_project', views.createProject, name='create-project'),
    # path('student/?/profile/update_project/<int:pk>', views.updateProject, name='update-project'),
    # path('student/?/profile/delete_project/<int:pk>', views.deleteProject, name='delete-project'),

]