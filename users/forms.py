from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth import get_user_model


class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', ]
