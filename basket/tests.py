import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import QueryDict
from django.urls import reverse
from django.utils import timezone

from catalogue.models import Product
from order.models import Discount
from .models import Basket, Line
from .views import BasketView, BasketAddView


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
    (discount_object, created) = Discount.objects.get_or_create(user=user,
                                                                available_from=timezone.now(),
                                                                available_until=timezone.now() + timezone.timedelta(
                                                                    days=7))
    return discount_object


@pytest.mark.django_db
class TestBasket:
    def test_basket_create(self, user):
        basket = Basket.objects.create(user=user)
        assert hasattr(basket, 'pk')
        assert not basket.is_submitted

    def test_basket_total_price(self, basket, line):
        assert basket.total_price == line.line_price

    def test_basket_view(self, rf, basket, line, user):
        url = reverse("basket_index")
        request = rf.get(url)
        request.user = user
        response = BasketView.as_view()(request)
        assert response.status_code == 200

    def test_basket_view_anonymous(self, rf):
        url = reverse("basket_index")
        request = rf.get(url)
        request.user = AnonymousUser()
        response = BasketView.as_view()(request)
        assert response.status_code == 302

    def test_add_to_basket(self, rf, user, product):
        url = reverse("basket_add")
        request = rf.get(url)
        request.user = user
        request.method = 'POST'
        request.POST = QueryDict('pk={}'.format(product.pk))
        BasketAddView.as_view()(request)
        assert request.user.basket.lines.exists()


@pytest.mark.django_db
class TestLine:
    def test_line_create(self, basket, product):
        line = Line.objects.create(basket=basket, product=product)
        assert hasattr(line, 'pk')
        assert line.quantity == 1

    def test_line_price(self, line):
        assert line.line_price == line.product.price
