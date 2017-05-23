from django import forms


class ProductRatingForm(forms.Form):
    rating = forms.IntegerField(widget=forms.Select(choices=[(i, i) for i in range(1, 6)]))
