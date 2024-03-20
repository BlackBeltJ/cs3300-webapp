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
        return render(request, 'profile_app/student_list.html', context={'list_of_students': list_of_students})
    
class StudentDetailView(generic.DetailView):
    model = Artist
    def studentDetail(request, pk):
        student = Artist.objects.get(pk=pk)
        print(f'student detail -> name: {student.name}, email: {student.email}, major: {student.instrument}')
        return render(request, 'profile_app/student_detail.html', context={'student': student})
    
class ProfileDetailView(generic.DetailView):
    model = Profile
    def profileDetail(request, pk):
        try: 
            profile = Profile.objects.get(pk=pk)
            student = Artist.objects.get(profile=profile)
            list_of_projects = Project.objects.select_related('profile').all().filter(profile=profile)
            print(f'profile detail -> profile name: {profile.title}, about: {profile.about}, contact email: {profile.contact_email}, list of projects: {list_of_projects}')        
        except profile.DoesNotExist:
            raise Http404('profile does not exist')
        
        return render(request, 'profile_app/profile_detail.html', context={'profile': profile, 'student': student, 'list_of_projects': list_of_projects})

class ProjectDetailView(generic.DetailView):
    model = Project
    def projectDetail(request, pk):
        try:
            project = Project.objects.get(pk=pk)
            profile = Profile.objects.get(project=project)
            student = Artist.objects.get(profile=profile)
            print(f'project detail -> project name: {project.title}, about: {project.description}, profile: {project.profile.title}')        
        except project.DoesNotExist:
            raise Http404('Project does not exist')
        
        return render(request, 'profile_app/project_detail.html', context={'project': project, 'student': student, 'profile': profile})

def editProfile(request, pk):
    student = Artist.objects.get(pk=pk)
    profile = student.profile  
    form = EditProfileForm(instance=profile) #request.GET
    
    if request.method == 'POST':
        profile_data = request.POST.copy()
        profile_data['student'] = student.id
        form = EditProfileForm(profile_data, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.student = student
            
            profile.save()
            #return redirect('profile-detail', pk) # either way works 
            return HttpResponseRedirect(reverse('profile-detail', args=[str(profile.id)]))
        
    context = {'form': form, 'profile': profile, 'student': student}
    return render(request, 'profile_app/profile_form.html', context)

def updateProject(request, pk):
    project = Project.objects.get(pk=pk)
    profile = Profile.objects.get(project=project)
    form = ProjectForm(instance=project) #request.GET
    
    if request.method == 'POST':
        project_data = request.POST.copy()
        project_data['profile'] = profile.id
        form = ProjectForm(project_data, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.profile = profile
            
            project.save()
            #return redirect('profile-detail', pk) # either way works 
            return HttpResponseRedirect(reverse('project-detail', args=[str(project.id)]))
        
    context = {'form': form, 'project': project, 'profile': profile}
    return render(request, 'profile_app/project_form.html', context)

def deleteProject(request, pk):
    project = Project.objects.get(pk=pk)
    profile = Profile.objects.get(project=project)
    student = Artist.objects.get(profile=profile)
    form = ProjectForm(instance=project) #request.GET... might want to change this line
    
    if request.method == 'POST':
        project.delete()
        return redirect('profile-detail', student.id) # either way works 
        #return HttpResponseRedirect(reverse('profile-detail', args=[str(profile.id)]))
        
    context = {'form': form, 'project': project}
    return render(request, 'profile_app/delete_project_form.html', context)

# Create a new project for a profile
def createProject(request, pk):
    form = ProjectForm()
    profile = Profile.objects.get(pk=pk)
    student = Artist.objects.get(profile=profile)

    if request.method == 'POST':
        project_data = request.POST.copy()
        project_data['profile'] = pk
        form = ProjectForm(project_data)
        if form.is_valid():
            project = form.save(commit=False)
            project.profile = profile
            project.save()
            
            return redirect('profile-detail', student.id)
        
    context = {'form': form, 'profile': profile, 'student': student}
    return render(request, 'profile_app/create_project_form.html', context)
