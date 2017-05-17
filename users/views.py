from django.views.generic.edit import CreateView, UpdateView

from .forms import UserCreationForm
from .models import User


class UserCreationView(CreateView):
    model = User
    form_class = UserCreationForm
    context_object_name = 'form'
    success_url = '/'
    template_name = 'users/sign_up.html'


class UserUpdateView(UpdateView):
    template_name = 'users/profile.html'
    model = User
    success_url = '/'
    fields = ['address', ]

    def get_object(self, queryset=None):
        return self.request.user
