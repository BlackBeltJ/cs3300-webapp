from django.urls import reverse
from django.contrib.auth.models import User
from music_app.models import Artist, Profile, Post

# selenium 4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

options = webdriver.ChromeOptions()
chrome_browser = webdriver.Chrome(options=options)


#browser.get('https://www.selenium.dev/documentation/')
#assert 'selenium' in browser.title

#elem = browser.find_element(By.NAME, 'p')
#elem.send_keys('selenium' + Keys.RETURN)

#browser.quit()
