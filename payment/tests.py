import datetime

import pytest
from django.contrib.auth import get_user_model
from django.http import QueryDict
from django.urls import reverse

from basket.models import Basket, Line
from catalogue.models import Product
from order.models import Order
from order.views import OrderCreate
from payment.models import Payment


@pytest.fixture
def user():
    user_model = get_user_model()
    (user_object, created) = user_model.objects.get_or_create(
        username='test_user')
    return user_object


@pytest.fixture
def product():
    (product_object, created) = Product.objects.get_or_create(
        name='Product',
        description="description",
        price=100, num_in_stock=1)
    return product_object


@pytest.fixture
def basket(user):
    (basket_object, created) = Basket.objects.get_or_create(user=user)
    return basket_object


@pytest.fixture
def line(user, basket, product):
    (line_object, created) = Line.objects.get_or_create(basket=basket,
                                                        product=product)
    return line_object


@pytest.fixture
def order(basket):
    (order_object, created) = Order.objects.get_or_create(basket=basket)
    return order_object


@pytest.mark.django_db
def test_payment(rf, order, user, line):
    url = reverse("checkout")
    request = rf.get(url)
    request.user = user
    line.basket = request.user.basket
    request.method = 'POST'
    card = '4242424242424242'
    exp = datetime.date.today() + datetime.timedelta(days=365)
    exp_month = exp.month
    exp_year = exp.year
    cvc = '9999'

    request.POST = QueryDict(
        'number={}&expiration_month={}&expiration_year={}&cvc={}'.format(card,
                                                                         exp_month,
                                                                         exp_year,
                                                                         cvc))
    OrderCreate.as_view()(request)
    assert Payment.objects.exists() and Payment.objects.all()[0].charge_id
