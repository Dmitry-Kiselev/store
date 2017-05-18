from datetime import date, datetime
from calendar import monthrange

from django import forms

from .models import Payment


class PaymentForm(forms.Form):
    number = forms.CharField(required=True, label="Card Number")
    expiration = forms.CharField(required=True, label="Expiration")
    cvc = forms.IntegerField(required=True, label="CCV Number",
                             max_value=9999,
                             widget=forms.TextInput(attrs={'size': '4'}))

    def clean(self):
        cleaned_data = super(PaymentForm, self).clean()
        if cleaned_data['number'] and (
                        len(cleaned_data['number']) < 13 or len(
                    cleaned_data['number']) > 16):
            raise forms.ValidationError("Please enter in a valid " + \
                                        "credit card number.")

        return cleaned_data
