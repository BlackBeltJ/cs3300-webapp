from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from music_app.views import *
from music_app.models import Artist, Profile, Post

User = get_user_model()

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        test_user1 = User.objects.create_user(
            username='testuser', password='password123')
        test_user1.save()
        
        # init an artist
        self.artist = Artist.objects.create(
            name="Test Artist",
            email="testy@email.com",
            genre="Rock",
            instrument="Guitar",
            user=self.user,
        )
        self.artist.save()
        
        self.post = Post.objects.create(
            title="Test Post",
            description="This is a test post.",
            profile=self.artist.profile
        )
        self.post.save()
    
    # Add more view tests here for other views like ArtistList, ArtistDetail, etc.
    # Ensure you test for both success and failure cases
    
    # 302 vs 200 code: https://umbraco.com/knowledge-base/http-status-codes/#:~:text=The%20200%20OK%20status%20code,in%20without%20the%20message%20body. 
    # 302 is a redirect status code, while 200 is a success status code.
    
class HomepageViewsTestCase(ViewsTestCase):    
    def setUp(self):
        self.client = Client()
        test_user1 = User.objects.create_user(
            username='testuser', password='password123')
        test_user1.save()
        
        # init an artist
        self.artist = Artist.objects.create(
            name="Test Artist",
            email="testy@email.com",
            genre="Rock",
            instrument="Guitar",
            user=test_user1,
        )
        self.artist.save()
        
        self.post = Post.objects.create(
            title="Test Post",
            description="This is a test post.",
            profile=self.artist.profile
        )
        self.post.save()
    
    def test_index_view_by_address_if_not_logged_in(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/accounts/login/?next=/')
        
    def test_index_view_logged_in(self):
        login = self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('index'))
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200) # 302 or 200
        #print(f"\n\nresponse: {response}")
        self.assertTemplateUsed(response, 'music_app/index.html')
        
    def test_index_view_by_name_logged_in(self):
        login = self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('index'))
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200) # 302 or 200
        #print(f"\n\nresponse: {response}")
        self.assertTemplateUsed(response, 'music_app/index.html')
    
    def test_artist_list_view(self):    
        login = self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('artists'))
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200) # 302 or 200
        #print(f"\n\nresponse content: {response.content}")
        self.assertTemplateUsed(response, 'music_app/artist_list.html')
    
class ArtistViewTestCase(ViewsTestCase):
    def setUp(self):
        self.client = Client()
        test_user1 = User.objects.create_user(
            username='testuser', password='password123')
        test_user1.save()
        
        # init an artist
        self.artist = Artist.objects.create(
            name="Test Artist",
            email="testy@email.com",
            genre="Rock",
            instrument="Guitar",
            user=test_user1,
        )
        self.artist.save()
        
        self.post = Post.objects.create(
            title="Test Post",
            description="This is a test post.",
            profile=self.artist.profile
        )
        self.post.save()
            
    def test_artist_detail_view_not_logged_in(self):
        response = self.client.get(reverse('artist-detail', args=[self.artist.id]))
        self.assertRedirects(response, '/accounts/login/?next=/artists/1')
    
    def test_create_post_view(self):
        login = self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('create-post', args=[self.artist.id]))
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200) # 302 or 200
        self.assertTemplateUsed(response, 'music_app/create_post_form.html')
        
    def test_artist_detail_view_logged_in(self):
        login = self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('artist-detail', args=[self.artist.id]))
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200) # 302 or 200
        
        self.assertTemplateUsed(response, 'music_app/artist_detail.html')

class ProfileViewTestCase(ViewsTestCase):
    def setUp(self):
        self.client = Client()
        test_user1 = User.objects.create_user(
            username='testuser', password='password123')
        test_user1.save()
        
        # init an artist
        self.artist = Artist.objects.create(
            name="Test Artist",
            email="testy@email.com",
            genre="Rock",
            instrument="Guitar",
            user=test_user1,
        )
        self.artist.save()
        
        self.post = Post.objects.create(
            title="Test Post",
            description="This is a test post.",
            profile=self.artist.profile
        )
        self.post.save()
        
    def test_profile_detail_view_not_logged_in(self):
        response = self.client.get(reverse('profile-detail', args=[self.artist.id]))
        self.assertRedirects(response, '/accounts/login/?next=/artists/1/profile')
    
    def test_profile_detail_view_logged_in(self):
        login = self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('profile-detail', args=[self.artist.id]))
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200) # 302 or 200
        self.assertTemplateUsed(response, 'music_app/profile_detail.html')
        
    def test_edit_profile_view(self):
        login = self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('edit-profile', args=[self.artist.id]))
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200) # 302 or 200
        self.assertTemplateUsed(response, 'music_app/profile_form.html')
        
class PostViewTestCase(ViewsTestCase):
    def setUp(self):
        self.client = Client()
        test_user1 = User.objects.create_user(
            username='testuser', password='password123')
        test_user1.save()
        
        # init an artist
        self.artist = Artist.objects.create(
            name="Test Artist",
            email="testy@email.com",
            genre="Rock",
            instrument="Guitar",
            user=test_user1,
        )
        self.artist.save()
        
        self.post = Post.objects.create(
            title="Test Post",
            description="This is a test post.",
            profile=self.artist.profile
        )
        self.post.save()
        
    def test_post_detail_view_not_logged_in(self):
        response = self.client.get(reverse('post-detail', args=[self.post.id]))
        self.assertRedirects(response, f'/accounts/login/?next=/artist/%253F/profile/post/1')
        
    def test_post_detail_view_logged_in(self):
        login = self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('post-detail', args=[self.post.id]))
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music_app/post_detail.html')
        
    def test_update_post_view(self):
        login = self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('update-post', args=[self.artist.id, self.post.id]))
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music_app/post_form.html')
        
    def test_delete_post_view(self):
        login = self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('delete-post', args=[self.artist.id, self.post.id]))
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music_app/delete_post_form.html')
        
    def test_create_post_view(self):
        login = self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('create-post', args=[self.artist.id]))
        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music_app/create_post_form.html')
        
class RegisterViewTestCase(ViewsTestCase):
    def setUp(self):
        self.client = Client()
        test_user1 = User.objects.create_user(
            username='testuser', password='password123')
        test_user1.save()
        
        # init an artist
        self.artist = Artist.objects.create(
            name="Test Artist",
            email="testy@email.com",
            genre="Rock",
            instrument="Guitar",
            user=test_user1,
        )
        self.artist.save()
        
        self.post = Post.objects.create(
            title="Test Post",
            description="This is a test post.",
            profile=self.artist.profile
        )
        self.post.save()
        
    def test_register_view(self):
        response = self.client.get(reverse('register-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        
class LoginViewTestCase(ViewsTestCase):
    def setUp(self):
        self.client = Client()
        test_user1 = User.objects.create_user(
            username='testuser', password='password123')
        test_user1.save()
        
        # init an artist
        self.artist = Artist.objects.create(
            name="Test Artist",
            email="testy@email.com",
            genre="Rock",
            instrument="Guitar",
            user=test_user1,
        )
        self.artist.save()
        
        self.post = Post.objects.create(
            title="Test Post",
            description="This is a test post.",
            profile=self.artist.profile
        )
        self.post.save()
    
    def test_login_view(self):
        response = self.client.get(reverse('login-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        
class LogoutViewTestCase(ViewsTestCase):
    def setUp(self):
        self.client = Client()
        test_user1 = User.objects.create_user(
            username='testuser', password='password123')
        test_user1.save()
        
        # init an artist
        self.artist = Artist.objects.create(
            name="Test Artist",
            email="testy@email.com",
            genre="Rock",
            instrument="Guitar",
            user=test_user1,
        )
        self.artist.save()
        
        self.post = Post.objects.create(
            title="Test Post",
            description="This is a test post.",
            profile=self.artist.profile
        )
        self.post.save()
        
    def test_logout_view(self):
        response = self.client.get(reverse('logout-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/logged_out.html')

        