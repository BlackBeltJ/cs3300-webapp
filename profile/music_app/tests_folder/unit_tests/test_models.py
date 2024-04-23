from django.test import TestCase
from django.contrib.auth.models import User
from music_app.models import Artist, Profile, Post
import re

class ModelTestCase(TestCase):    
    def setUp(self):
        # init a user 
        self.user = User.objects.create_user(
            username='testuser', password='password123')
        
        # init an artist
        self.artist = Artist.objects.create(
            name="Test Artist",
            email="testy@email.com",
            genre="Rock",
            instrument="Guitar",
            # link user to artist
            user=self.user,
        )
        
        # link artist to profile
        self.profile = self.artist.profile
        
        # create a post
        self.post = Post.objects.create(
            title="Test Post",
            description="This is a test post.",
            # link post to profile
            profile=self.profile
        )
    
    # unit tests for artist creation
    def test_artist_creation(self):
        self.assertEqual(self.artist.name, "Test Artist")
        self.assertEqual(self.artist.email, "testy@email.com")
        self.assertEqual(self.artist.genre, "Rock")
        self.assertEqual(self.artist.instrument, "Guitar")
        self.assertEqual(str(self.profile), self.profile.title)
        self.assertEqual(self.profile.get_absolute_url(), f'/artists/{self.artist.id}/profile')
        self.assertEqual(self.artist.profile, self.profile)
        self.assertEqual(self.artist.user, self.user)
        
    # unit tests for post creation
    def test_post_creation(self):
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.description, "This is a test post.")
        self.assertEqual(self.post.profile, self.profile)
        self.assertEqual(str(self.post), self.post.title)
        # test that default_audio.mp3 is the default audio file
        self.assertEqual(self.post.get_base_mp3_filename(), 'default_audio.mp3')
        
        # regex for any three characters
        expected_url = f'/artist/???/profile/post/{self.post.id}'
        actual_url = self.post.get_absolute_url()
        # split up the url to isolate the last portion for comparison
        start_index = expected_url.find('/artist/') + len('/artist/')
        end_index = expected_url.find('/profile/')
        expected_url_without_artist = expected_url[:start_index] + '...' + expected_url[end_index:]
        actual_url_without_artist = actual_url[:start_index] + '...' + actual_url[end_index:]
        self.assertEqual(actual_url_without_artist, expected_url_without_artist)
    
    # unit tests for profile creation
    def test_profile_creation(self):
        self.assertEqual(self.profile.title, f"{self.artist.name}'s Profile")
        self.assertEqual(self.profile.is_public, True)
        self.assertEqual(self.profile.about, f"This is a new profile for {self.artist.name}")
        self.assertEqual(self.profile.contact_email, "testy@email.com")
        self.assertEqual(str(self.profile), self.profile.title)
        self.assertEqual(self.profile.get_absolute_url(), f'/artists/{self.artist.id}/profile')
        self.assertEqual(self.profile, self.artist.profile)
        
    