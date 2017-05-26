import math

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from basket.models import Basket, Line
from catalogue.models import Product
from .models import Order, Discount
from .views import OrderCreate


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
def discount(user):
    (discount_object, created) = Discount.objects.get_or_create(owner=user,
                                                                available_from=timezone.now(),
                                                                available_until=timezone.now() + timezone.timedelta(
                                                                    days=7),
                                                                value=10)
    return discount_object


@pytest.fixture
def order(basket):
    (order_object, created) = Order.objects.get_or_create(basket=basket)
    return order_object


@pytest.mark.django_db
class TestOrder:
    def test_order_create(self, basket):
        order = Order.objects.create(basket=basket)
        assert hasattr(order, 'pk')
        assert order.status == Order.ORDER_STATUS.PENDING

    def test_order_discount(self, order, discount, product):
        Line.objects.create(basket=order.basket, product=product)
        order.discount = discount
        assert order.get_discount_val == (
            order.basket.total_price - order.basket.total_price_inc_discount)

        order.discount.in_percent = True
        assert math.ceil(order.get_discount_val) == math.ceil(
            order.basket.total_price - order.basket.total_price_inc_discount)

    def test_order_view(self, rf, user, line):
        url = reverse("checkout")
        request = rf.get(url)
        request.user = user
        line.basket = request.user.basket
        response = OrderCreate.as_view()(request)
        assert response.status_code == 200
