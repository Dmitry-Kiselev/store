"""restaurant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from .views import IndexTemplateView, ProductListView, ProductDetailView, \
    ProductRatingView, FeedbackView

urlpatterns = [
    url(r'^$', IndexTemplateView.as_view(), name='index'),
    url(r'^catalogue/$', ProductListView.as_view(), name='catalogue'),
    url(r'^catalogue/(?P<category>\d+)$', ProductListView.as_view(),
        name='catalogue'),
    url(r'^product/(?P<pk>\d+)', ProductDetailView.as_view(),
        name='product_detail'),
    url(r'catalogue/rating/(?P<pk>\d+)$', ProductRatingView.as_view(),
        name='rating'),
    url(r'catalogue/feedback/(?P<pk>\d+)$', FeedbackView.as_view(),
        name='feedback'),
]
