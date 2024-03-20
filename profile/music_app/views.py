from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.http import Http404
from django.shortcuts import redirect
from .models import *
from .forms import *

def index(request):
    # Render index.html
    artist_active_profiles = Artist.objects.select_related('profile').all().filter(profile__is_active=True)
    print('active profile query set', artist_active_profiles)
    #context is dictionary that is passed as a template ("variable") to the html file
    return render(request, 'music_app/index.html', {'artist_active_profiles': artist_active_profiles})

#def redirect(request, context):
#    return render(request)

class StudentListView(generic.ListView):
    model = Artist
    def displayStudents(request):
        list_of_students = Artist.objects.all()
        print('list of students', list_of_students)
        return render(request, 'portfolio_app/student_list.html', context={'list_of_students': list_of_students})
    
class StudentDetailView(generic.DetailView):
    model = Artist
    def studentDetail(request, pk):
        student = Artist.objects.get(pk=pk)
        print(f'student detail -> name: {student.name}, email: {student.email}, major: {student.instrument}')
        return render(request, 'portfolio_app/student_detail.html', context={'student': student})
    
class PortfolioDetailView(generic.DetailView):
    model = Profile
    def portfolioDetail(request, pk):
        try: 
            portfolio = Profile.objects.get(pk=pk)
            student = Artist.objects.get(portfolio=portfolio)
            list_of_projects = Project.objects.select_related('portfolio').all().filter(portfolio=portfolio)
            print(f'portfolio detail -> portfolio name: {portfolio.title}, about: {portfolio.about}, contact email: {portfolio.contact_email}, list of projects: {list_of_projects}')        
        except portfolio.DoesNotExist:
            raise Http404('Portfolio does not exist')
        
        return render(request, 'portfolio_app/portfolio_detail.html', context={'portfolio': portfolio, 'student': student, 'list_of_projects': list_of_projects})

class ProjectDetailView(generic.DetailView):
    model = Project
    def projectDetail(request, pk):
        try:
            project = Project.objects.get(pk=pk)
            portfolio = Profile.objects.get(project=project)
            student = Artist.objects.get(portfolio=portfolio)
            print(f'project detail -> project name: {project.title}, about: {project.description}, portfolio: {project.portfolio.title}')        
        except project.DoesNotExist:
            raise Http404('Project does not exist')
        
        return render(request, 'portfolio_app/project_detail.html', context={'project': project, 'student': student, 'portfolio': portfolio})

def editPortfolio(request, pk):
    student = Artist.objects.get(pk=pk)
    portfolio = student.profile  
    form = EditPortfolioForm(instance=portfolio) #request.GET
    
    if request.method == 'POST':
        portfolio_data = request.POST.copy()
        portfolio_data['student'] = student.id
        form = EditPortfolioForm(portfolio_data, instance=portfolio)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.student = student
            
            portfolio.save()
            #return redirect('portfolio-detail', pk) # either way works 
            return HttpResponseRedirect(reverse('portfolio-detail', args=[str(portfolio.id)]))
        
    context = {'form': form, 'portfolio': portfolio, 'student': student}
    return render(request, 'portfolio_app/portfolio_form.html', context)

def updateProject(request, pk):
    project = Project.objects.get(pk=pk)
    portfolio = Profile.objects.get(project=project)
    form = ProjectForm(instance=project) #request.GET
    
    if request.method == 'POST':
        project_data = request.POST.copy()
        project_data['portfolio'] = portfolio.id
        form = ProjectForm(project_data, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.portfolio = portfolio
            
            project.save()
            #return redirect('portfolio-detail', pk) # either way works 
            return HttpResponseRedirect(reverse('project-detail', args=[str(project.id)]))
        
    context = {'form': form, 'project': project, 'portfolio': portfolio}
    return render(request, 'portfolio_app/project_form.html', context)

def deleteProject(request, pk):
    project = Project.objects.get(pk=pk)
    portfolio = Profile.objects.get(project=project)
    student = Artist.objects.get(portfolio=portfolio)
    form = ProjectForm(instance=project) #request.GET... might want to change this line
    
    if request.method == 'POST':
        project.delete()
        return redirect('portfolio-detail', student.id) # either way works 
        #return HttpResponseRedirect(reverse('portfolio-detail', args=[str(portfolio.id)]))
        
    context = {'form': form, 'project': project}
    return render(request, 'portfolio_app/delete_project_form.html', context)

# Create a new project for a portfolio
def createProject(request, pk):
    form = ProjectForm()
    portfolio = Profile.objects.get(pk=pk)
    student = Artist.objects.get(portfolio=portfolio)

    if request.method == 'POST':
        project_data = request.POST.copy()
        project_data['portfolio'] = pk
        form = ProjectForm(project_data)
        if form.is_valid():
            project = form.save(commit=False)
            project.portfolio = portfolio
            project.save()
            
            return redirect('portfolio-detail', student.id)
        
    context = {'form': form, 'portfolio': portfolio, 'student': student}
    return render(request, 'portfolio_app/create_project_form.html', context)
