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
#from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService



class HostTest(LiveServerTestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(options=options)
        self.browser.implicitly_wait(10)
        self.browser.get(self.live_server_url)
        self.browser.maximize_window()

    def tearDown(self):
        self.browser.quit()

    def test_home_page(self):
        # options = webdriver.ChromeOptions()
        # chrome_browser = webdriver.Chrome(options=options)
        
        self.browser.get('http://localhost:8000/')
        #self.browser.get(reverse('index'))
        #time.sleep(5)
        wait = WebDriverWait(self.browser, 10)
        wait.until(lambda condition: self.browser.current_url != 'http://localhost:8000/')
        wait.until(EC.title_contains('Artist'))
        
        assert 'Artist' in self.browser.title
    
    def test_artist_page(self):
        self.browser.get('http://localhost:8000/artists/')
        wait = WebDriverWait(self.browser, 10)
        wait.until(lambda condition: self.browser.current_url != 'http://localhost:8000/artists/')
        wait.until(EC.title_contains('Artist'))
        
        assert 'Artist' in self.browser.title

class LoginFormTest(LiveServerTestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(options=options)
        self.browser.implicitly_wait(5)
        self.browser.set_page_load_timeout(5)
        self.browser.get(self.live_server_url)
        self.browser.maximize_window()
        
    def test_login_form(self):
        """
        Django Admin login test
        """
        # Open the admin index page
        self.browser.get('http://localhost:8000/accounts/login')


        # Fill login information of the user
        username = self.browser.find_element(By.NAME, 'username')
        password = self.browser.find_element(By.NAME, 'password')
        submit = self.browser.find_element(By.ID, 'submit')
        
        time.sleep(3)
        username.send_keys('admin')
        password.send_keys('admin')
        
        time.sleep(3)
        #wait = WebDriverWait(self.browser, 5)
        submit.send_keys(Keys.RETURN)

        #wait.until(lambda condition: self.browser.current_url != 'http://localhost:8000/accounts/login/?next=/accounts/login/')
        #wait.until(EC.title_contains('Artist'))
        assert 'admin' in self.browser.page_source

        # Selenium knows it has to wait for page loads (except for AJAX requests)
        # so we don't need to do anything about that, and can just
        # call find_css. Since we can chain methods, we can
        # call the built-in send_keys method right away to change the
        # value of the field
        #      self.wd.find_css('#id_username').send_keys("admin")
        # for the password, we can now just call find_css since we know the page
        # has been rendered
        #      self.wd.find_css("#id_password").send_keys('pw')
        # You're not limited to CSS selectors only, check
        # http://seleniumhq.org/docs/03_webdriver.html for 
        # a more comprehensive documentation.
        #        self.wd.find_element_by_xpath('//input[@value="Log in"]').click()
        # Again, after submiting the form, we'll use the find_css helper
        # method and pass as a CSS selector, an id that will only exist
        # on the index page and not the login page
        #        self.wd.find_css("#content-main")

    # def test_login(self):
    #     self.browser.get(self.live_server_url)
    #     self.assertIn('Home', self.browser.title)
    #     self.browser.find_element_by_link_text('Login').click()
    #     self.assertIn('Login', self.browser.title)
    #     username = self.browser.find_element_by_id('id_username')
    #     username.send_keys('testuser')
    #     password = self.browser.find_element_by_id('id_password')
    #     password.send_keys('testpassword')
    #     self.browser.find_element_by_id('submit').click()
    #     self.assertIn('Home', self.browser.title)

    # def test_register(self):
    #     self.browser.get(self.live_server_url)
    #     self.assertIn('Home', self.browser.title)
    #     self.browser.find_element_by_link_text('Register').click()
    #     self.assertIn('Register', self.browser.title)
    #     username = self.browser.find_element_by_id('id_username')
    #     username.send_keys('testuser')
    #     email = self.browser.find_element_by_id('id_email')
    #     email.send_keys('tesy@email.com')
    #     password = self.browser.find_element_by_id('id_password')
    #     password.send_keys('testpassword')
    #     password2 = self.browser.find_element_by_id('id_password2')
    #     password2.send_keys('testpassword')
    #     self.browser.find_element_by_id('submit').click()
    #     self.assertIn('Home', self.browser.title)
        

   # chrome_browser.get('https://www.selenium.dev/documentation/')
   # assert 'selenium' in chrome_browser.title

#    elem = chrome_browser.find_element(By.NAME, 'p')
 #   elem.send_keys('selenium' + Keys.RETURN)

  #  chrome_browser.quit()
