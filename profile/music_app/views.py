from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.http import Http404
from django.views import generic
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from .decorators import *

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
        profile_form = ProfileForm()
        
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
    
    @login_required
    def displayArtists(request):
        list_of_artists = Artist.objects.all()
        print('list of artists', list_of_artists)
        return render(request, 'music_app/artist_list.html', context={'list_of_artists': list_of_artists})
    
    @login_required
    def artistDetail(request, pk):
        artist = Artist.objects.get(pk=pk)
        print(f'artist detail -> name: {artist.name}, email: {artist.email}, genre: {artist.genre}, profile: {artist.profile.title}')
        return render(request, 'music_app/artist_detail.html', context={'artist': artist})
    
    @login_required
    #@allowed_users(allowed_roles=['artist'])
    def userPage(request, pk):
        artist = Artist.objects.get(pk=pk)
        print(f'artist detail -> name: {artist.name}, email: {artist.email}, genre: {artist.genre}, profile: {artist.profile.title}')
        return render(request, 'music_app/artist_detail.html', context={'artist': artist})
    
        artist = request.user.artist
        form = ArtistForm(instance=artist)
        print('artist', artist)
        profile = artist.profile
        print('profile', profile)
        if request.method == 'POST':
            form = ArtistForm(request.POST, request.FILES, instance=artist)
            if form.is_valid():
                form.save()
                
        context = {'form': form, 'profile': profile}
        return render(request, 'music_app/artist_detail.html', context)
    
class ProfileOperations(LoginRequiredMixin, generic.DetailView):
    model = Profile
    
    @login_required
    def profileDetail(request, pk):
        try: 
            artist = Artist.objects.get(pk=pk)
            print(f"artist id: {artist.id}, artist profile: {artist.profile}")
            profile = artist.profile
            # profile = Profile.objects.get(pk=artist.profile)
            list_of_projects = Project.objects.select_related('profile').all().filter(profile=profile)
            print(f'profile detail -> profile name: {profile.title}, about: {profile.about}, contact email: {profile.contact_email}, list of projects: {list_of_projects}')        
        except profile.DoesNotExist:
            raise Http404('profile does not exist')
        
        return render(request, 'music_app/profile_detail.html', context={'profile': profile, 'artist': artist, 'list_of_projects': list_of_projects})

    @login_required
    def editProfile(request, pk):
        artist = Artist.objects.get(pk=pk)
        print(f"artist id: {artist.id}, artist profile: {artist.profile}")
        profile = artist.profile
        form = ProfileForm(instance=profile) #request.GET
        
        if request.method == 'POST':
            profile_data = request.POST.copy()
            #profile_data['artist'] = artist.id
            form = ProfileForm(profile_data, instance=profile)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.artist = artist
                
                profile.save()
                #return redirect('profile-detail', pk) # either way works 
                return HttpResponseRedirect(reverse('profile-detail', args=[str(artist.id)]))
            
        context = {'form': form, 'profile': profile, 'artist': artist}
        return render(request, 'music_app/profile_form.html', context)

class ProjectOperations(LoginRequiredMixin, generic.DetailView, generic.edit.UpdateView, generic.edit.DeleteView, generic.edit.CreateView):
    model = Project
    
    @login_required
    def projectDetail(request, pk):
        try:
            project = Project.objects.get(pk=pk)
            profile = Profile.objects.get(project=project)
            artist = Artist.objects.get(profile=profile)
            print(f'project detail -> project name: {project.title}, about: {project.description}, profile: {project.profile.title}')        
        except project.DoesNotExist:
            raise Http404('Project does not exist')
        
        return render(request, 'music_app/project_detail.html', context={'project': project, 'artist': artist, 'profile': profile})

    @login_required
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

    @login_required
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
    @login_required
    def createProject(request, pk):
        form = ProjectForm()
        artist = Artist.objects.get(pk=pk)
        print(f"artist id: {artist.id}, artist profile: {artist.profile}")
        profile = artist.profile

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

class ArtistAuth(generic.DetailView):
    model = Artist
    def loginPage(request):
        return render(request, 'music_app/login.html')
    
    def logoutPage(request):
        return render(request, 'registration/logged_out.html')
    
    def registerPage(request):
        user_data = CreateUserForm()
        artist_form = ArtistForm()
        profile_form = ProfileForm()
        
        if request.method == 'POST':
            user_data = CreateUserForm(request.POST)
            user_form = ArtistForm(user_data)
            #form = request.POST.copy()
            if user_data.is_valid():
                user = user_data.save(commit=False)
                username = user_data.cleaned_data.get('username')
                group = Group.objects.get(name='artist_role')
                user.groups.add(group)
                artist = Artist.objects.create(user=user,)
                #profile = Profile.objects.create()
                #artist.profile = profile
                artist.save()
                user_form.save()
                
                messages.success(request, 'Account was created for ' + username)
                return redirect('login')
            
        context = {'form': user_data}
        return render(request, 'registration/register.html', context)

# class UserOperations(generic.edit.CreateView):
#     model = User
#     def createUser(request):
#         user_form = UserCreationForm()
#         artist_form = ArtistForm()
#         profile_form = ProfileForm()
        
#         if request.method == 'POST':
#             user_form = UserCreationForm(request.POST)
#             if user_form.is_valid():
                
#                 #createArtistAndProfile()
                    
#                     # create a new artist for user
#                     # create new profile for artist
#                 user_form.save()
#             return redirect('login')
            
#         context = {'form': user_form}
#         return render(request, 'music_app/create_user_form.html', context)