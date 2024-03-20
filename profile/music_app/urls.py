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
    path('', views.index, name='login'),
    path('', views.index, name='logout'),
    path('students/', views.StudentListView.displayStudents, name='students'),
    path('student/<int:pk>', views.StudentDetailView.studentDetail, name='student-detail'),
    path('student/<int:pk>/portfolio', views.PortfolioDetailView.portfolioDetail, name='portfolio-detail'),
    #.as_view() is a method that returns a default view function
    path('student/?/portfolio/project/<int:pk>', views.ProjectDetailView.projectDetail, name='project-detail'),
    path('student/<int:pk>/portfolio/edit', views.editPortfolio, name='edit-portfolio'),
    #<uuid:pk> is a path converter that matches a UUID
    path('student/<int:pk>/portfolio/create_project', views.createProject, name='create-project'),
    path('student/?/portfolio/update_project/<int:pk>', views.updateProject, name='update-project'),
    path('student/?/portfolio/delete_project/<int:pk>', views.deleteProject, name='delete-project'),

]