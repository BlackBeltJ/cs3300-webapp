from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from music_app.models import Artist, Profile, Post

class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password123')
        
        # init an artist
        self.artist = Artist.objects.create(
            name="Test Artist",
            email="testy@email.com",
            genre="Rock",
            instrument="Guitar",
            user=self.user,
        )
        
        self.post = Post.objects.create(
            title="Test Post",
            description="This is a test post.",
            profile=self.artist.profile
        )
        
    def test_index_view(self):
        client = Client()
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music_app/index.html')
        
    # Add more view tests here for other views like ArtistList, ArtistDetail, etc.
    # Ensure you test for both success and failure cases
    
    def test_artist_list_view(self):    
        client = Client()
        response = client.get(reverse('artists'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music_app/artist_list.html')
    
    def test_artist_detail_view(self):
        client = Client()
        response = client.get(reverse('artist-detail', args=[self.artist.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music_app/artist_detail.html')
        
    def test_create_post_view(self):
        client = Client()
        response = client.get(reverse('create-post', args=[self.artist.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music_app/post_form.html')
        
        data = {'title': 'Test Post', 'description': 'This is a test post.'}
        response = client.post(reverse('create-post', args=[self.artist.id]), data)
        self.assertEqual(response.status_code, 302) # expected redirect after successful form submission
        
    def test_create_post_view_invalid_form(self):
        client = Client()
        response = client.get(reverse('create-post', args=[self.artist.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music_app/post_form.html')
        
        data = {'title': '', 'description': 'This is a test post.'}
        response = client.post(reverse('create-post', args=[self.artist.id]), data)
        self.assertEqual(response.status_code, 200)
        
    