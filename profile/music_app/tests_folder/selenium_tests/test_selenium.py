from django.urls import reverse
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from music_app.models import Artist, Profile, Post
from music_app.views import *
import time

# selenium 4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

class HostTest(LiveServerTestCase):
    # setup function gets called automatically before every test
    def setUp(self):
        options = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(options=options)
        # browser settings
        self.browser.implicitly_wait(10)
        self.browser.get(self.live_server_url)
        self.browser.maximize_window()

    def tearDown(self):
        self.browser.quit()

    def test_home_page(self):
        # get home page
        self.browser.get('http://localhost:8000/')
        wait = WebDriverWait(self.browser, 10)
        # wait until page is fully loaded
        wait.until(lambda condition: self.browser.current_url == 'http://localhost:8000/' or 'http://localhost:8000/accounts/login/?next=/')
        assert 'Artist' in self.browser.title
        
    def test_login_page(self):
        # get login page
        self.browser.get('http://localhost:8000/accounts/login')
        wait = WebDriverWait(self.browser, 10)
        # wait until page is fully loaded
        wait.until(lambda condition: self.browser.current_url == 'http://localhost:8000/accounts/login' or 'http://localhost:8000/accounts/login/?next=/')
        assert 'Register' in self.browser.page_source

class LoginFormTest(LiveServerTestCase):
    # setup function gets called automatically before every test
    def setUp(self):
        options = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(options=options)
        self.browser.implicitly_wait(5)
        self.browser.set_page_load_timeout(5)
        self.browser.get(self.live_server_url)
        self.browser.maximize_window()
        
    def test_login_form(self):
        # get login page
        self.browser.get('http://localhost:8000/accounts/login')

        # Fill login information of the user
        username = self.browser.find_element(By.NAME, 'username')
        password = self.browser.find_element(By.NAME, 'password')
        submit = self.browser.find_element(By.NAME, 'submit')
        
        # the following lines will enter in the login information
        # wait a second before entering login info
        time.sleep(1)
        username.send_keys('testUser')
        password.send_keys('testpassword')
        wait = WebDriverWait(self.browser, 5)
        submit.send_keys(Keys.RETURN)

        # wait until page is fully loaded
        wait.until(lambda condition: self.browser.current_url != 'http://localhost:8000/accounts/login/?next=/accounts/login/')
        assert 'testUser' in self.browser.page_source

class YourProfilePageTest(LiveServerTestCase):  
    # setup function gets called automatically before every test
    def setUp(self):
        options = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(options=options)
        self.browser.implicitly_wait(5)
        self.browser.set_page_load_timeout(5)
        self.browser.get(self.live_server_url)
        self.browser.maximize_window()
        
        # first login
        self.browser.get('http://localhost:8000/accounts/login')

        # Fill login information of the user
        username = self.browser.find_element(By.NAME, 'username')
        password = self.browser.find_element(By.NAME, 'password')
        submit = self.browser.find_element(By.NAME, 'submit')
        
        # enter login info
        time.sleep(1)
        username.send_keys('testUser')
        password.send_keys('testpassword')
        submit.send_keys(Keys.RETURN)
        
    def test_your_profile_page(self):
        # reset back to home page
        time.sleep(1)
        self.browser.get('http://localhost:8000/')
        
        # go to your profile  
        wait = WebDriverWait(self.browser, 5)     
        # wait until page is fully loaded
        wait.until(lambda condition: self.browser.current_url != 'http://localhost:8000/accounts/login/')
        yourProfile = self.browser.find_element(By.NAME, 'yourProfile')
        yourProfile.send_keys(Keys.RETURN)
        
        # wait until page is fully loaded
        wait.until(lambda condition: self.browser.current_url != 'http://localhost:8000/')
        assert 'test1' in self.browser.page_source # 'test1' is testUser's profile name, checking that the profile page is correct

    def test_artist_page(self):
        self.browser.get('http://localhost:8000/artists/')
        wait = WebDriverWait(self.browser, 5)
        # wait until page is fully loaded
        wait.until(lambda condition: self.browser.current_url == 'http://localhost:8000/artists/')
        assert 'List of artists' in self.browser.page_source
        
    def test_profile_page(self):
        self.browser.get('http://localhost:8000/artists/37/profile')
        wait = WebDriverWait(self.browser, 5)
        # wait until page is fully loaded
        wait.until(lambda condition: self.browser.current_url == 'http://localhost:8000/artists/37/profile')
        assert 'test1' in self.browser.page_source
        
    def test_post_page(self):
        self.browser.get('http://localhost:8000/artist/37/profile/create_post')
        wait = WebDriverWait(self.browser, 5)
        # wait until page is fully loaded
        wait.until(lambda condition: self.browser.current_url == 'http://localhost:8000/artist/37/profile/create_post')
        assert 'Create new post' in self.browser.page_source
