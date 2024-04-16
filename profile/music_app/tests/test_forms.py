from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from music_app.models import Artist, Profile, Post
from music_app.forms import ArtistForm, ProfileForm, PostForm

class PostFormTestCase(TestCase):
    def test_valid_form(self):
        data = {
            'title': "Test Post",
            'description': "description"
        }
        form = PostForm(data=data)
        self.assertTrue(form.is_valid())
        
    def test_missing_title_invalid(self):
        data = {'title': "", 'description': "description"}
        form = PostForm(data=data)
        self.assertFalse(form.is_valid() and self.assertIn('title', form.errors))
