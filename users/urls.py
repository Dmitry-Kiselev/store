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
from django.contrib.auth.views import LoginView, LogoutView

from .views import UserCreationView, UserUpdateView

urlpatterns = [
    url(r'^sing_up/', UserCreationView.as_view(), name='sign_up'),
    url(r'^login/',
        LoginView.as_view(template_name='users/sign_up.html', success_url='/'),
        name='login'),
    url(r'^logout/', LogoutView.as_view(next_page='/'), name='logout'),
    url(r'^profile/$', UserUpdateView.as_view(), name='edit_profile')
]
