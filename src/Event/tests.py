from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from .models import Event, Representation
from Account.models import User

from CollegeBook.tests import BaseTest
from Account.tests import AccountTest


class EventTest(StaticLiveServerTestCase):
    @staticmethod
    def init_create_event(self):
        driver = BaseTest.init(self)
        AccountTest.init_user()
        AccountTest.login_user(driver)
        link = driver.find_element(By.ID, 'nav-create-event')
        link.click()
        box_name = driver.find_element(By.NAME, 'name')
        box_desc = driver.find_element(By.NAME, 'description')
        box_user = driver.find_element(By.NAME, 'user')
        box_option = box_user.find_element(By.TAG_NAME, 'option')
        box_date = driver.find_element(By.NAME, 'date')
        box_submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        box_name.send_keys('test_name')
        box_desc.send_keys('test_description')
        box_option.click()
        box_date.click()
        box_day = driver.find_element(By.CSS_SELECTOR,
                                      "span[aria-label='March 9, 2023']")  # change the month to actual
        box_day.click()
        box_submit.send_keys(Keys.RETURN)
        return driver
    def test_create_event(self):
        driver = BaseTest.init(self)
        AccountTest.init_user()
        AccountTest.login_user(driver)
        link = driver.find_element(By.ID, 'nav-create-event')
        link.click()
        box_name = driver.find_element(By.NAME, 'name')
        box_desc = driver.find_element(By.NAME, 'description')
        box_user = driver.find_element(By.NAME, 'user')
        box_option =  box_user.find_element(By.TAG_NAME, 'option')
        box_date = driver.find_element(By.NAME, 'date')
        box_submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        box_name.send_keys('test_name')
        box_desc.send_keys('test_description')
        box_option.click()
        box_date.click()
        box_day = driver.find_element(By.CSS_SELECTOR,"span[aria-label='March 9, 2023']") # change the month to actual
        box_day.click()
        box_submit.send_keys(Keys.RETURN)
        assert 'test_name' in driver.page_source
        driver.close()

    def test_event_details(self):
        driver = EventTest.init_create_event(self)
        link = driver.find_element(By.LINK_TEXT, 'Details')
        link.click()
        assert 'Liste des représentations' in driver.page_source
        driver.close()

    def test_delete_rep(self):
        driver = EventTest.init_create_event(self)
        link = driver.find_element(By.ID, 'nav-personnal-events')
        link.click()
        box_delete = driver.find_element(By.CSS_SELECTOR, "svg[class='bi bi-x-circle']")
        box_delete.click()
        assert 'Souhaitez vous vraiment supprimer l\'event' in driver.page_source
        box_non = driver.find_element(By.ID,'id_choix_1')
        box_non.click()
        box_submit = driver.find_element(By.CSS_SELECTOR,"input[type='submit']")
        box_submit.click()
        assert 'Vos événements' in driver.page_source
        box_delete = driver.find_element(By.CSS_SELECTOR, "svg[class='bi bi-x-circle']")
        box_delete.click()
        box_oui = driver.find_element(By.ID,'id_choix_0')
        box_oui.click()
        box_submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        box_submit.click()
        assert '9 mars 2023' not in driver.page_source
        driver.close()

    def test_update_rep(self):
        driver = EventTest.init_create_event(self)
        link = driver.find_element(By.ID, 'nav-personnal-events')
        link.click()
        box_update = driver.find_element(By.CSS_SELECTOR, "svg[class='bi bi-pencil-square']")
        box_update.click()
        assert 'Changer' in driver.page_source
        box_date = driver.find_element(By.ID,'id_date')
        box_date.click()
        box_date = driver.find_element(By.CSS_SELECTOR, "span[aria-label='March 9, 2023']")  # change the month to actual
        box_date.click()
        box_hour = driver.find_element(By.CSS_SELECTOR,"input[class='numInput flatpickr-hour']")
        box_hour.send_keys('14')
        box_submit = driver.find_element(By.CSS_SELECTOR,"input[type='submit']")
        box_submit.send_keys(Keys.RETURN)
        assert '2023 14:00' in driver.page_source
        driver.close()

