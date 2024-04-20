from django.test import TestCase
from django.contrib.auth.models import User
from music_app.models import Artist, Profile, Post
import re

class ModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Artist.objects.create(name="Test Artist",
        #     email="testy@email.com",
        #     genre="Rock",
        #     instrument="Guitar",
        #     #user=self.user,
        # )
        pass
        #print("setUpTestData: Run once to set up non-modified data for all class methods.")
        #return super().setUpTestData()
        
    # def test_false_is_false(self):
    #     print("Method: test_false_is_false.")
    #     self.assertFalse(False)
            
    # def test_false_is_true(self):
    #     print("Method: test_false_is_true.")
    #     self.assertTrue(False)
            
    # def test_true_is_true(self):
    #     print("Method: test_true_is_true.")
    #     self.assertTrue(True)
    
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
        
        # profile should automatically be created with artist
        # # init a profile
        # self.profile = Profile.objects.create(
        #     title="Test Profile",
        #     is_public=True,
        #     about="This is a test profile.",
        #     contact_email="email@email.com"
        # )
        self.profile = self.artist.profile
        
        # create a post
        self.post = Post.objects.create(
            title="Test Post",
            description="This is a test post.",
            profile=self.profile
        )
        
        #print("setUp: Run once for every test method to setup clean data.")
        #return super().setUp()
    
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
        self.assertEqual(self.post.get_base_mp3_filename(), 'default_audio.mp3')
        # print(self.post.get_absolute_url())
        # print(f'/artist/{self.artist.id}/profile/post/{self.post.id}/')
        expected_url = f'/artist/???/profile/post/{self.post.id}'
        actual_url = self.post.get_absolute_url()
        start_index = expected_url.find('/artist/') + len('/artist/')
        end_index = expected_url.find('/profile/')
        expected_url_without_artist = expected_url[:start_index] + '...' + expected_url[end_index:]
        actual_url_without_artist = actual_url[:start_index] + '...' + actual_url[end_index:]
        # print(f'actual_url: {actual_url}')
        # print(f'expected_url: {expected_url}')
        # print(f'expected_url_without_artist: {expected_url_without_artist}')
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
        
    