from django.conf.urls import url, include
from api.catalogue import views as catalogue_view
from rest_framework.routers import DefaultRouter
from api.order import views as order_views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'products', catalogue_view.ProductViewSet)
router.register(r'categories', catalogue_view.CategoryViewSet)
router.register(r'orders', order_views.OrderViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
]