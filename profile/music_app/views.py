from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.http import Http404
from django.views import generic
#from django.views import View
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from .models import *
from .forms import *
from .decorators import *

#@login_required(login_url='login')
def index(request):
    artist_active_profiles = Artist.objects.select_related('profile').all().filter(profile__is_public=True)
    print('active profile query set', artist_active_profiles)
    #context is dictionary that is passed as a template ("variable") to the html file
    return render(request, 'music_app/index.html', {'artist_active_profiles': artist_active_profiles})

def get_current_user(request):
    current_user = request.user
    return current_user

#def redirect(request, context):
#    return render(request)
    
class ArtistOperations(LoginRequiredMixin, generic.ListView, generic.DetailView, generic.edit.CreateView, generic.edit.DeleteView):
    model = Artist
    
    # quick function if I need to create an artist without a user
    # @login_required
    # def createArtistAndProfile(request):
    #     artist_form = ArtistForm()
    #     profile_form = ProfileForm()
        
    #     if request.method == 'POST':
    #         artist_data = request.POST.copy()
    #         artist_form = ArtistForm(artist_data)
    #         if artist_form.is_valid():
    #             artist = artist_form.save(commit=False)
    #             artist.save()
    #             context = {'artist_form': artist_form, 'profile_form': profile_form, 'artist': artist}
    #             return redirect('artist-detail', artist.id)
        
    #     context = {'artist_form': artist_form, 'profile_form': profile_form}
    #     return render(request, 'music_app/create_artist_form.html', context)
    
    @login_required
    @user_is_owner()
    def deleteArtistAndProfile(request, pk):
        artist = Artist.objects.get(pk=pk)
        profile = Profile.objects.get(artist=artist)
        artist_form = ArtistForm(instance=artist)
        
        if request.method == 'POST':
            profile.delete() # I chose to delete the profile because it has the relationship set up to cascade delete the artist too
            return redirect('index')

        context = {'artist_form': artist_form, 'artist': artist, 'profile': profile}
        return render(request, 'music_app/delete_artist_form.html', context)
    
    @login_required
    #@allowed_users(allowed_roles=['artist_role'])
    def displayArtists(request):
        list_of_artists = Artist.objects.select_related('profile').all().filter(profile__is_public=True)
        print('list of artists', list_of_artists)
        return render(request, 'music_app/artist_list.html', context={'list_of_artists': list_of_artists})
    
    ## decorators and permissions
    @login_required(login_url='login')
    #@allowed_users(allowed_roles=['artist_role'])
    def artistDetail(request, pk):
        artist = Artist.objects.get(pk=pk)
        # if artist.has_perm('can_view_artist', get_current_user(request)):
        print(f'artist detail -> name: {artist.name}, email: {artist.email}, genre: {artist.genre}, profile: {artist.profile.title}')
        context={'artist': artist}
        return render(request, 'music_app/artist_detail.html', context)

        # redirect to list of artists
        #return render(request, 'music_app/artist_detail.html', context)
    
    @login_required(login_url='login')
    @user_is_owner()
    def editArtist(request, pk):
        artist = Artist.objects.get(pk=pk)
        form = ArtistForm(instance=artist)
        
        if request.method == 'POST':
            artist_data = request.POST.copy()
            form = ArtistForm(artist_data, instance=artist)
            if form.is_valid():
                artist = form.save(commit=False)
                artist.save()
                return redirect('artist-detail', artist.id)
            
        context = {'form': form, 'artist': artist}
        return render(request, 'music_app/artist_form.html', context)
    
    @login_required(login_url='login')
    def artistDetailFromBase(request, user_pk):
        user_ = get_object_or_404(User, pk = user_pk)
        artist = Artist.objects.get(user=user_)
        # if artist.has_perm('can_view_artist', get_current_user(request)):
        print(f'artist detail -> name: {artist.name}, email: {artist.email}, genre: {artist.genre}, profile: {artist.profile.title}')
        context={'artist': artist}
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
            list_of_posts = Post.objects.select_related('profile').all().filter(profile=profile)
            print(f'profile detail -> profile name: {profile.title}, about: {profile.about}, contact email: {profile.contact_email}, list of posts: {list_of_posts}')        
        except profile.DoesNotExist:
            raise Http404('profile does not exist')
        
        context={'profile': profile, 'artist': artist, 'list_of_posts': list_of_posts}
        return render(request, 'music_app/profile_detail.html', context)

    @login_required
    @user_is_owner()
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

class PostOperations(LoginRequiredMixin, generic.DetailView, generic.edit.UpdateView, generic.edit.DeleteView, generic.edit.CreateView):
    model = Post
    
    @login_required
    def postDetail(request, pk):
        try:
            post = Post.objects.get(pk=pk)
            profile = Profile.objects.get(post=post)
            artist = Artist.objects.get(profile=profile)
            print(f'post detail -> post name: {post.title}, about: {post.description}, mp3_file: {post.mp3_file}, profile: {post.profile.title}')        
        except post.DoesNotExist:
            raise Http404('Post does not exist')
        
        context={'post': post, 'artist': artist, 'mp3_file': post.mp3_file, 'profile': profile}
        return render(request, 'music_app/post_detail.html', context)

    @login_required
    @user_is_owner()
    def updatePost(request, post_pk, pk):
        artist = Artist.objects.get(pk=pk)
        post = Post.objects.get(pk=post_pk)
        profile = Profile.objects.get(post=post)
        form = PostForm(instance=post)
        
        if request.method == 'POST':
            post_data = request.POST.copy()
            post_data['profile'] = profile.id
            form = PostForm(post_data, request.FILES, instance=post)
            print(f'mp3_file {form["mp3_file"]}')
            if form.is_valid():
                post = form.save(commit=False)
                post.profile = profile
                post.save()
                print(f"post was updated successfully, mp3_file: {post.mp3_file}")
                return HttpResponseRedirect(reverse('post-detail', args=[str(post.id)]))
            
        context = {'MEDIA_URL': settings.MEDIA_URL, 'form': form, 'post': post, 'profile': profile, 'artist': artist}
        return render(request, 'music_app/post_form.html', context)

    @login_required
    @user_is_owner()
    def deletePost(request, post_pk, pk):
        artist = Artist.objects.get(pk=pk)
        post = Post.objects.get(pk=post_pk)
        profile = Profile.objects.get(post=post)
        form = PostForm(instance=post)
        
        if request.method == 'POST':
            post.delete()
            return redirect('profile-detail', artist.id)
            
        context = {'form': form, 'post': post, 'artist': artist, 'profile': profile}
        return render(request, 'music_app/delete_post_form.html', context)

    # Create a new post for a profile
    @login_required
    @user_is_owner()
    def createPost(request, pk):
        form = PostForm()
        artist = Artist.objects.get(pk=pk)
        print(f"artist id: {artist.id}, artist profile: {artist.profile}")
        profile = artist.profile

        if request.method == 'POST':
            post_data = request.POST.copy()
            post_data['profile'] = pk
            form = PostForm(post_data, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.profile = profile
                post.save()
                
                return redirect('profile-detail', artist.id)
            
        context = {'form': form, 'profile': profile, 'artist': artist}
        return render(request, 'music_app/create_post_form.html', context)

class ArtistAuth(generic.DetailView):
    model = Artist
    def loginPage(request):
        return render(request, 'music_app/login.html')
    
    def logoutPage(request):
        return render(request, 'registration/logged_out.html')
    
    def registerPage(request):
        user_form = CreateUserForm()
        artist_form = ArtistForm()
        
        if request.method == 'POST':
            user_form = CreateUserForm(request.POST)
            #user_data = request.POST.copy()
            #user_form = CreateUserForm(user_data)
            
            artist_form = ArtistForm(request.POST)
            #artist_form = request.POST.copy()
            #artist_form = ArtistForm(artist_data)
            
            if user_form.is_valid() and artist_form.is_valid():
                user = user_form.save()
                user.save()
                artist = artist_form.save(commit=False)
                artist.user = user
                artist.save()
                username = user_form.cleaned_data.get('username')
                group = Group.objects.get(name='artist_role')
                user.groups.add(group)
                #artist.groups.add(group)
                print(f'user detail -> username: {user.username}, email: {user.email}')
                print(f'artist detail -> name: {artist.name}, email: {artist.email}, genre: {artist.genre}, instrument: {artist.instrument}, profile: {artist.profile.title}')
                messages.success(request, 'Account was created for ' + username)
                return redirect('artist-detail', artist.id)
            
        context = {'user_form': user_form, 'artist_form': artist_form}
        return render(request, 'registration/register.html', context)
