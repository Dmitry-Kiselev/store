from django.views.generic.edit import CreateView

from .forms import UserCreationForm
from .models import User


class UserCreationView(CreateView):
    model = User
    form_class = UserCreationForm
    context_object_name = 'form'
    success_url = '/'
    template_name = 'users/sing_up.html'
