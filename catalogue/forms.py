from django import forms

from .models import ProductFeedback


class ProductRatingForm(forms.Form):
    rating = forms.IntegerField(
        widget=forms.Select(choices=[(i, i) for i in range(1, 6)]))


class ProductFeedbackForm(forms.ModelForm):
    class Meta:
        model = ProductFeedback
        fields = ['email', 'feedback']
