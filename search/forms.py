from django import forms
from haystack.forms import SearchForm as HaystackSearchForm


class SearchForm(HaystackSearchForm):
    q = forms.CharField(required=False, label='',
                        widget=forms.TextInput(attrs={'type': 'search'}))
