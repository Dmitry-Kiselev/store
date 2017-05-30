import datetime

from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from catalogue.models import Product


class TestUser(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(TestUser, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(TestUser, self).tearDown()

    def test_full(self):
        self._test_registration()
        self._test_login()
        self._test_add_to_basket()
        self._test_make_order()

    def _test_registration(self):

        selenium = self.selenium

        User = get_user_model()

        try:
            user = User.objects.get(username='mytestuser')
            user.delete()
        except User.DoesNotExist:
            pass

        # Opening the link we want to test
        url = 'http://127.0.0.1:8000' + reverse('sign_up')
        index_url = 'http://127.0.0.1:8000' + reverse('index')
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

        wait = WebDriverWait(selenium, 10)  # wait for redirect
        wait.until(lambda
                       driver: selenium.current_url != url)

        assert selenium.current_url != url

    def _test_login(self):

        selenium = self.selenium
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

        wait = WebDriverWait(selenium, 10)  # wait for redirect
        wait.until(lambda
                       driver: selenium.current_url != url)

        assert selenium.current_url != url

    def _test_add_to_basket(self):

        selenium = self.selenium

        product = Product.objects.create(pk=4, price=1000,
                                         name='Product',
                                         description='Description',
                                         num_in_stock=12)
        url = 'http://127.0.0.1:8000' + reverse('product_detail',
                                                kwargs={'pk': product.pk})
        selenium.get(url)
        submit = selenium.find_element_by_id('submit')
        submit.send_keys(Keys.RETURN)

        wait = WebDriverWait(selenium, 10)  # wait for redirect
        wait.until(lambda
                       driver: selenium.current_url != url)

        assert selenium.current_url != url

    def _test_make_order(self):

        selenium = self.selenium

        url = 'http://127.0.0.1:8000' + reverse('checkout')
        selenium.get(url)

        number = selenium.find_element_by_id('id_number')
        expiration_month = selenium.find_element_by_id(
            'id_expiration_month')
        expiration_year = selenium.find_element_by_id(
            'id_expiration_year')
        cvc = selenium.find_element_by_id('id_cvc')
        submit = selenium.find_element_by_id('submit')

        exp = datetime.date.today() + datetime.timedelta(days=365)

        number.send_keys('4242424242424242')
        expiration_month.send_keys(exp.month)
        expiration_year.send_keys(exp.year)
        cvc.send_keys('9999')

        submit.send_keys(Keys.RETURN)

        wait = WebDriverWait(selenium, 10)  # wait for redirect
        wait.until(lambda
                       driver: selenium.current_url != url)

        assert selenium.current_url != url
