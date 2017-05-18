from django import forms
from django.forms.models import modelformset_factory

from .models import Line


class LineForm(forms.ModelForm):
    class Meta:
        model = Line
        fields = ['quantity']


BasketLineFormSet = modelformset_factory(Line, form=LineForm, extra=0,
                                         can_delete=True, fields=['quantity'])
