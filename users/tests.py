import datetime
import time

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


@pytest.mark.django_db
class TestUser:
    selenium = webdriver.Firefox()

    @pytest.mark.order1
    def test_registration(self):
        User = get_user_model()

        User.objects.filter(username='mytestuser').delete()

        # Opening the link we want to test
        url = 'http://127.0.0.1:8000' + reverse('sign_up')
        TestUser.selenium.get(url)
        # find the form element
        username = TestUser.selenium.find_element_by_id('id_username')
        password1 = TestUser.selenium.find_element_by_id('id_password1')
        password2 = TestUser.selenium.find_element_by_id('id_password2')

        submit = TestUser.selenium.find_element_by_id('submit')

        username.send_keys('mytestuser')
        password1.send_keys('123456qwerty')
        password2.send_keys('123456qwerty')

        submit.send_keys(Keys.RETURN)

        time.sleep(5)  # wait for redirect

        assert TestUser.selenium.current_url != url

    @pytest.mark.order2
    def test_login(self):
        # Opening the link we want to test
        url = 'http://127.0.0.1:8000' + reverse('login')
        TestUser.selenium.get(url)
        # find the form element
        username = TestUser.selenium.find_element_by_id('id_username')
        password = TestUser.selenium.find_element_by_id('id_password')
        submit = TestUser.selenium.find_element_by_id('submit')
        username.send_keys('mytestuser')
        password.send_keys('123456qwerty')
        submit.send_keys(Keys.RETURN)

        time.sleep(5)  # wait for redirect

        assert TestUser.selenium.current_url != url

    @pytest.mark.order3
    def test_add_to_basket(self, product):
        url = 'http://127.0.0.1:8000' + reverse('product_detail',
                                                kwargs={'pk': product.pk})
        TestUser.selenium.get(url)
        submit = TestUser.selenium.find_element_by_id('submit')
        submit.send_keys(Keys.RETURN)

        time.sleep(5)  # wait for redirect

        assert TestUser.selenium.current_url != url

    @pytest.mark.order4
    def test_make_order(self):
        url = 'http://127.0.0.1:8000' + reverse('checkout')
        TestUser.selenium.get(url)

        number = TestUser.selenium.find_element_by_id('id_number')
        expiration_month = TestUser.selenium.find_element_by_id(
            'id_expiration_month')
        expiration_year = TestUser.selenium.find_element_by_id(
            'id_expiration_year')
        cvc = TestUser.selenium.find_element_by_id('id_cvc')
        submit = TestUser.selenium.find_element_by_id('submit')

        exp = datetime.date.today() + datetime.timedelta(days=365)

        number.send_keys('4242424242424242')
        expiration_month.send_keys(exp.month)
        expiration_year.send_keys(exp.year)
        cvc.send_keys('9999')

        submit.send_keys(Keys.RETURN)

        time.sleep(5)  # wait for redirect

        assert TestUser.selenium.current_url != url
