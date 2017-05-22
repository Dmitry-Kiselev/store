from django import forms


class PaymentForm(forms.Form):
    number = forms.CharField(required=True, label="Card Number")
    expiration_month = forms.CharField(required=True, label="Expiration month")
    expiration_year = forms.CharField(required=True, label="Expiration year")
    cvc = forms.IntegerField(required=True, label="CCV Number",
                             max_value=9999,
                             widget=forms.TextInput(attrs={'size': '4'}))

    provider = None

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(PaymentForm, self).clean()
        if not self.validate_card(cleaned_data['number']):
            raise forms.ValidationError("Please enter in a valid " + \
                                        "credit card number.")

        return cleaned_data

    def validate_card(self, number):
        digits = [int(i) for i in str(number)]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        total = sum(odd_digits)
        for digit in even_digits:
            total += sum([int(i) for i in str(2 * digit)])
        return total % 10 == 0
