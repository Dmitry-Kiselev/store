from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth import get_user_model
from django import forms


class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', ]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['address', 'address_lat', 'address_lng',]
        widgets = {
            'address_lat': forms.HiddenInput(attrs={'id': 'lat'}),
            'address_lng': forms.HiddenInput(attrs={'id': 'lng'}),
        }
