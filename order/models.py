from django.db import models
from django.db.models import QuerySet

from basket.models import Basket
from catalogue.models import TimeStampedModel
from django.utils import timezone
from django.conf import settings
import stripe


class Order(TimeStampedModel):
    class ORDER_STATUS:
        PENDING = 0
        FAILED = 1
        PROCESSING = 2
        COMPLETED = 3

        STATUS_CHOICES = (
            (PENDING, 'Pending payment'),
            (FAILED, 'Failed'),
            (PROCESSING, 'Processing'),
            (COMPLETED, 'Completed')
        )

    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=ORDER_STATUS.STATUS_CHOICES,
                                      default=ORDER_STATUS.PENDING)
    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL,
                                 blank=True, null=True)

    def __str__(self):
        return 'Order {}'.format(self.pk)

    @property
    def total_price(self):
        if not self.discount:
            return self.basket.total_price

        if self.discount.in_percent:
            return self.basket.total_price * ((100 - self.discount.value) / 100)
        else:
            return self.basket.total_price - self.discount.value

    @property
    def get_discount_val(self):
        if not self.discount:
            return 0
        if self.discount.in_percent:
            return self.basket.total_price - (
                self.basket.total_price * ((100 - self.discount.value) / 100))
        else:
            return self.basket.total_price - (
                self.basket.total_price - self.discount.value)


class DiscountQuerySet(QuerySet):
    def get_active_discounts(self):
        now = timezone.now()
        return self.filter(available_from__gte=now, available_until__lte=now)


class Discount(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='discounts')
    value = models.DecimalField(max_digits=6, decimal_places=2)
    in_percent = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)
    available_from = models.DateTimeField()
    available_until = models.DateTimeField()

    objects = DiscountQuerySet.as_manager()

    def is_active(self):
        now = timezone.now()
        return self.available_from >= now and self.available_until <= now

    def __str__(self):
        return '{} {}'.format(self.value, self.owner.username)


class Payment(models.Model):
    charge_id = models.CharField(max_length=32)
    charged_sum = models.DecimalField(max_digits=10, decimal_places=2)
    discount_sum = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True,
                              null=True)

    def __init__(self, *args, **kwargs):
        super(Payment, self).__init__(*args, **kwargs)
        stripe.api_key = settings.STRIPE_API_KEY
        self.stripe = stripe

        if self.order:
            self.charged_sum = self.order.total_price
            self.discount_sum = self.order.get_discount_val

    def charge(self, number, exp_month, exp_year, cvc):
        """
        Takes a the price and credit card details: number, exp_month,
        exp_year, cvc.

        Returns a tuple: (Boolean, Class) where the boolean is if
        the charge was successful, and the class is response (or error)
        instance.
        """

        if self.charge_id:  # don't let this be charged twice!
            return False, Exception("Already charged.")

        try:
            response = self.stripe.Charge.create(
                amount=int(self.charged_sum * 1000),
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

        return True
