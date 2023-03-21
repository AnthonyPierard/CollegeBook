from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from .models import User

from CollegeBook.tests import BaseTest
class AccountTest(StaticLiveServerTestCase):
    @staticmethod
    def init_superuser():
        User.objects.create_superuser('admin@test.com', 'testpassword');

    @staticmethod
    def init_user():
        User.objects.create_user('user@test.com', 'testpassword');

    @staticmethod
    def login_superuser(driver):
        link = driver.find_element(By.ID, 'nav-login')
        link.click()
        box_email = driver.find_element(By.NAME, 'email')
        box_pwd = driver.find_element(By.NAME, 'password')
        box_submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        box_email.send_keys('admin@test.com')
        box_pwd.send_keys('testpassword')
        box_submit.send_keys(Keys.RETURN)

    @staticmethod
    def login_user(driver):
        link = driver.find_element(By.ID, 'nav-login')
        link.click()
        box_email = driver.find_element(By.NAME, 'email')
        box_pwd = driver.find_element(By.NAME, 'password')
        box_submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        box_email.send_keys('user@test.com')
        box_pwd.send_keys('testpassword')
        box_submit.send_keys(Keys.RETURN)

    def test_login_superuser(self):
        driver = BaseTest.init(self)
        AccountTest.init_superuser()
        AccountTest.login_superuser(driver)
        assert 'admins' in driver.page_source
        driver.close()

    def test_login_user(self):
        driver = BaseTest.init(self)
        AccountTest.init_user()
        AccountTest.login_user(driver)
        assert 'admins' not in driver.page_source
        driver.close()

    def test_logout_superuser(self):
        driver = BaseTest.init(self)
        AccountTest.init_superuser()
        AccountTest.login_superuser(driver)
        link = driver.find_element(By.ID,'nav-logout')
        link.click()
        assert 'Se connecter' in driver.page_source
        driver.close()

    def test_logout_user(self):
        driver = BaseTest.init(self)
        AccountTest.init_user()
        AccountTest.login_user(driver)
        link = driver.find_element(By.ID, 'nav-logout')
        link.click()
        assert 'Se connecter' in driver.page_source
        driver.close()

    def test_update_first_name_superuser(self):
        driver = BaseTest.init(self)
        AccountTest.init_superuser()
        AccountTest.login_superuser(driver)
        link = driver.find_element(By.ID, 'nav-account')
        link.click()
        box_first_name = driver.find_element(By.NAME, 'first_name')
        box_submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        box_first_name.send_keys('test_superuser')
        box_submit.send_keys(Keys.RETURN)
        link = driver.find_element(By.ID, 'nav-account')
        link.click()
        assert 'test_superuser' in driver.page_source

    def test_update_first_name_user(self):
        driver = BaseTest.init(self)
        AccountTest.init_user()
        AccountTest.login_user(driver)
        sleep(1)
        link = driver.find_element(By.ID, 'nav-account')
        link.click()
        box_first_name = driver.find_element(By.NAME, 'first_name')
        box_submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        box_first_name.send_keys('test_user')
        box_submit.send_keys(Keys.RETURN)
        link = driver.find_element(By.ID, 'nav-account')
        link.click()
        assert 'test_user' in driver.page_source


