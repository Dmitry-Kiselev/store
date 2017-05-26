import time

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


@pytest.mark.django_db
class TestUser:
    def test_registration(self):
        User = get_user_model()

        User.objects.filter(username='mytestuser').delete()

        selenium = webdriver.Firefox()
        # Opening the link we want to test
        url = 'http://127.0.0.1:8000' + reverse('sign_up')
        selenium.get(url)
        # find the form element
        username = selenium.find_element_by_id('id_username')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')

        submit = selenium.find_element_by_id('submit')

        username.send_keys('mytestuser')
        password1.send_keys('123456qwerty')
        password2.send_keys('123456qwerty')

        submit.send_keys(Keys.RETURN)

        time.sleep(5)  # wait for redirect

        assert selenium.current_url != url

    def test_login(self):
        selenium = webdriver.Firefox()
        # Opening the link we want to test
        url = 'http://127.0.0.1:8000' + reverse('login')
        selenium.get(url)
        # find the form element
        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('submit')
        username.send_keys('mytestuser')
        password.send_keys('123456qwerty')
        submit.send_keys(Keys.RETURN)

        time.sleep(5)  # wait for redirect

        assert selenium.current_url != url
