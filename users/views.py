from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView

from .forms import UserCreationForm, UserProfileForm
from .models import User


class UserCreationView(CreateView):
    model = User
    form_class = UserCreationForm
    context_object_name = 'form'
    success_url = '/'
    template_name = 'users/sign_up.html'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    model = User
    success_url = '/'
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user
