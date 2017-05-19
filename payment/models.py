import stripe
from django.conf import settings
from django.db import models

from order.models import Order
from django.conf import settings


class Payment(models.Model):
    class Meta:
        abstract = True

    charge_id = models.CharField(max_length=32)
    charged_sum = models.DecimalField(max_digits=10, decimal_places=2)
    discount_sum = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True,
                              null=True)

    def __init__(self, *args, **kwargs):
        super(Payment, self).__init__(*args, **kwargs)

        if self.order:
            self.charged_sum = self.order.total_price
            self.discount_sum = self.order.get_discount_val

    def charge(self, number, exp_month, exp_year, cvc):
        """
        Takes a the price and credit card details: number, exp_month,
        exp_year, cvc.

        Returns a tuple: (Boolean, Class) where the boolean is if
        the charge was successful
        """

        raise NotImplementedError()

    def __str__(self):
        return '{}'.format(self.charge_id)

    @staticmethod
    def get_payment_service():
        if settings.PAYMENT_SERVICE == 'stripe':
            return StripePayment


class StripePayment(Payment):
    def __init__(self, *args, **kwargs):
        super(StripePayment, self).__init__(*args, **kwargs)
        stripe.api_key = settings.STRIPE_API_KEY
        self.stripe = stripe

    def charge(self, number, exp_month, exp_year, cvc):

        if self.charge_id:  # don't let this be charged twice!
            return False, Exception("Already charged.")

        try:
            response = self.stripe.Charge.create(
                amount=int(self.charged_sum * 100),
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
            return False

        self.charge_id = response.stripe_id
        self.order.status = Order.ORDER_STATUS.PROCESSING
        self.order.save()
        self.save()

        return True
