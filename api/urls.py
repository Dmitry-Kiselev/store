from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from api.basket import views as basket_views
from api.catalogue import views as catalogue_view
from api.order import views as order_views
from api.payment import views as payment_views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'products', catalogue_view.ProductViewSet)
router.register(r'categories', catalogue_view.CategoryViewSet)
router.register(r'orders', order_views.OrderViewSet)
router.register(r'baskets', basket_views.BasketViewSet)
router.register(r'lines', basket_views.LineViewSet)
router.register(r'payment', payment_views.PaymentViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
]
