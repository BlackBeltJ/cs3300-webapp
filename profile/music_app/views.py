from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.http import Http404
from django.views import generic
from .models import *
from .forms import *

def index(request):
    artist_active_profiles = Artist.objects.select_related('profile').all().filter(profile__is_public=True)
    print('active profile query set', artist_active_profiles)
    #context is dictionary that is passed as a template ("variable") to the html file
    return render(request, 'music_app/index.html', {'artist_active_profiles': artist_active_profiles})

#def redirect(request, context):
#    return render(request)
    
class ArtistOperations(generic.ListView, generic.DetailView, generic.edit.CreateView, generic.edit.DeleteView):
    model = Artist
    def createArtistAndProfile(request):
        artist_form = ArtistForm()
        profile_form = EditProfileForm()
        
        if request.method == 'POST':
            artist_data = request.POST.copy()
            artist_form = ArtistForm(artist_data)
            if artist_form.is_valid():
                artist = artist_form.save(commit=False)
                artist.save()
                context = {'artist_form': artist_form, 'profile_form': profile_form, 'artist': artist}
                return redirect('artist-detail', artist.id)
        
        context = {'artist_form': artist_form, 'profile_form': profile_form}
        return render(request, 'music_app/create_artist_form.html', context)
    
    def deleteArtistAndProfile(request, pk):
        artist = Artist.objects.get(pk=pk)
        profile = Profile.objects.get(artist=artist)
        artist_form = ArtistForm(instance=artist)
        
        if request.method == 'POST':
            profile.delete() # I chose to delete the profile becasue it has the relationship set up to cascade delete the artist too
            return redirect('index')

        context = {'artist_form': artist_form, 'artist': artist, 'profile': profile}
        return render(request, 'music_app/delete_artist_form.html', context)
    
    def displayArtists(request):
        list_of_artists = Artist.objects.all()
        print('list of artists', list_of_artists)
        return render(request, 'music_app/artist_list.html', context={'list_of_artists': list_of_artists})
    
    def artistDetail(request, pk):
        artist = Artist.objects.get(pk=pk)
        print(f'artist detail -> name: {artist.name}, email: {artist.email}, genre: {artist.genre}, profile: {artist.profile.title}')
        return render(request, 'music_app/artist_detail.html', context={'artist': artist})
    
class ProfileOperations(generic.DetailView):
    model = Profile
    def profileDetail(request, pk):
        try: 
            profile = Profile.objects.get(pk=pk)
            artist = Artist.objects.get(profile=profile)
            list_of_projects = Project.objects.select_related('profile').all().filter(profile=profile)
            print(f'profile detail -> profile name: {profile.title}, about: {profile.about}, contact email: {profile.contact_email}, list of projects: {list_of_projects}')        
        except profile.DoesNotExist:
            raise Http404('profile does not exist')
        
        return render(request, 'music_app/profile_detail.html', context={'profile': profile, 'artist': artist, 'list_of_projects': list_of_projects})

    def editProfile(request, pk):
        artist = Artist.objects.get(pk=pk)
        profile = artist.profile  
        form = EditProfileForm(instance=profile) #request.GET
        
        if request.method == 'POST':
            profile_data = request.POST.copy()
            profile_data['artist'] = artist.id
            form = EditProfileForm(profile_data, instance=profile)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.artist = artist
                
                profile.save()
                #return redirect('profile-detail', pk) # either way works 
                return HttpResponseRedirect(reverse('profile-detail', args=[str(profile.id)]))
            
        context = {'form': form, 'profile': profile, 'artist': artist}
        return render(request, 'music_app/profile_form.html', context)

class ProjectOperations(generic.DetailView, generic.edit.UpdateView, generic.edit.DeleteView, generic.edit.CreateView):
    model = Project
    def projectDetail(request, pk):
        try:
            project = Project.objects.get(pk=pk)
            profile = Profile.objects.get(project=project)
            artist = Artist.objects.get(profile=profile)
            print(f'project detail -> project name: {project.title}, about: {project.description}, profile: {project.profile.title}')        
        except project.DoesNotExist:
            raise Http404('Project does not exist')
        
        return render(request, 'music_app/project_detail.html', context={'project': project, 'artist': artist, 'profile': profile})

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
        return render(request, 'music_app/project_form.html', context)

    def deleteProject(request, pk):
        project = Project.objects.get(pk=pk)
        profile = Profile.objects.get(project=project)
        artist = Artist.objects.get(profile=profile)
        form = ProjectForm(instance=project)
        
        if request.method == 'POST':
            project.delete()
            return redirect('profile-detail', artist.id) # either way works 
            #return HttpResponseRedirect(reverse('profile-detail', args=[str(profile.id)]))
            
        context = {'form': form, 'project': project}
        return render(request, 'music_app/delete_project_form.html', context)

    # Create a new project for a profile
    def createProject(request, pk):
        form = ProjectForm()
        profile = Profile.objects.get(pk=pk)
        artist = Artist.objects.get(profile=profile)

        if request.method == 'POST':
            project_data = request.POST.copy()
            project_data['profile'] = pk
            form = ProjectForm(project_data)
            if form.is_valid():
                project = form.save(commit=False)
                project.profile = profile
                project.save()
                
                return redirect('profile-detail', artist.id)
            
        context = {'form': form, 'profile': profile, 'artist': artist}
        return render(request, 'music_app/create_project_form.html', context)
    
class UserOperations(generic.edit.CreateView):
    model = User
    def createUser(request):
        user_form = UserCreationForm()
        artist_form = ArtistForm()
        profile_form = EditProfileForm()
        
        if request.method == 'POST':
            user_form = UserCreationForm(request.POST)
            if user_form.is_valid():
                
                #createArtistAndProfile()
                    
                    # create a new artist for user
                    # create new profile for artist
                user_form.save()
            return redirect('login')
            
        context = {'form': user_form}
        return render(request, 'music_app/create_user_form.html', context)