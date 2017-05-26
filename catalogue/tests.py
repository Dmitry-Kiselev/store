import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse

from .models import Product, Category, ProductFeedback, ProductRating
from .views import ProductDetailView


@pytest.fixture
def product():
    (product_object, created) = Product.objects.get_or_create(
        name='Product',
        description="description",
        price=100, num_in_stock=1)
    return product_object


@pytest.fixture
def user():
    user_model = get_user_model()
    (user_object, created) = user_model.objects.get_or_create(
        username='test_user')
    return user_object


@pytest.mark.django_db
class TestCategory:
    def test_category_create(self):
        category = Category.objects.create(name='Category', )
        assert hasattr(category, 'pk')


@pytest.mark.django_db
class TestProduct:
    def test_product_create(self):
        product = Product.objects.create(name='Product',
                                         description="description",
                                         price=100, num_in_stock=1)
        assert hasattr(product, 'pk')

    def test_product_view(self, rf):
        (product_object, created) = Product.objects.get_or_create(
            name='Product',
            description="description",
            price=100, num_in_stock=1)
        kwargs = {
            'pk': product_object.pk,
        }
        url = reverse("product_detail", kwargs=kwargs)
        request = rf.get(url)
        request.user = AnonymousUser()
        response = ProductDetailView.as_view()(request, **kwargs)
        assert response.status_code == 200

    def test_product_rating(self, product, user):
        ProductRating.objects.create(rated_product=product, user=user, rating=5)
        ProductRating.objects.create(rated_product=product, user=user, rating=1)
        assert product.rating == 3

    def test_product_rating_anonymous(self, product):
        exception_happened = False
        try:
            ProductRating.objects.create(rated_product=product,
                                         user=AnonymousUser(), rating=5)
        except ValueError:
            exception_happened = True

        assert exception_happened

    def test_product_anonymous_feedback(self, product):
        feedback = ProductFeedback.objects.create(feedback_product=product,
                                                  feedback='text',
                                                  email='example@ex.com')
        assert feedback.status == ProductFeedback.FEEDBACK_STATUS.NEW
        assert hasattr(feedback, 'pk')

    def test_product_user_feedback(self, product, user):
        feedback = ProductFeedback.objects.create(feedback_product=product,
                                                  feedback='text', user=user)
        assert feedback.status == ProductFeedback.FEEDBACK_STATUS.NEW
        assert hasattr(feedback, 'pk')


