from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from .models import Event,Representation
from Account.models import User

from CollegeBook.tests import BaseTest
from Account.tests import AccountTest

class EventTest(StaticLiveServerTestCase):
    @staticmethod
    def init_create_event(self):
        event = Event.model(name='event test',description='description test')
        event.save()
        rep = Representation.model(event=event)
        rep.save()
        #jsp si ca fonctionne

    # def test_create_event(self):
    #     driver = BaseTest.init(self)
    #     AccountTest.init_user()
    #     AccountTest.login_user(driver)
    #     link = driver.find_element(By.ID,'nav-create-event')
    #     link.click()
    #     box_name = driver.find_element(By.NAME,'name')
    #     box_desc = driver.find_element(By.NAME,'description')
    #     box_user = driver.find_element(By.NAME,'user')
    #     box_submit = driver.find_element(By.CSS_SELECTOR,"input[type='submit']")
    #     box_name.send_keys('test_name')
    #     box_desc.send_keys('test_description')
    #     box_user.send_keys()
    #     box_submit.send_keys(Keys.RETURN)
    #     assert 'Les événements' in driver.page_source
    #     driver.close()