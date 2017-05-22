from abc import ABC

import stripe
from django.conf import settings


class AbstractProvider(ABC):

    charge_id = None

    def charge(self, number, exp_month, exp_year, cvc, charged_sum):
        raise NotImplementedError


class StripeProvider(AbstractProvider):
    def __init__(self, *args, **kwargs):
        super(StripeProvider, self).__init__(*args, **kwargs)
        stripe.api_key = settings.STRIPE_API_KEY
        self.stripe = stripe

    def charge(self, number, exp_month, exp_year, cvc, charged_sum):

        if self.charge_id:  # don't let this be charged twice!
            return Exception("Already charged.")

        try:
            response = self.stripe.Charge.create(
                amount=int(charged_sum * 100),
                currency="uah",
                card={
                    "number": number,
                    "exp_month": exp_month,
                    "exp_year": exp_year,
                    "cvc": cvc,
                },
                description='Thank you for your purchase!')

        except self.stripe.CardError as ce:
            # charge failed
            return ce

        self.charge_id = response.stripe_id
        return self.charge_id


def get_payment_provider():
    if settings.PAYMENT_SERVICE == 'stripe':
        return StripeProvider