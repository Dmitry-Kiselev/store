from _decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import QuerySet
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from basket.models import Basket
from catalogue.models import TimeStampedModel, Product
from .tasks import send_email


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
        shipping_price = self.basket.shipping_price
        if not self.discount:
            return self.basket.total_price + Decimal(shipping_price)

        if self.discount.in_percent:
            return self.basket.total_price * (
                (100 - self.discount.value) / 100) + shipping_price
        else:
            return self.basket.total_price - self.discount.value + Decimal(shipping_price)

    @property
    def get_discount_val(self):
        if not self.discount:
            return 0
        if self.discount.in_percent:
            return self.basket.total_price - (
                self.basket.total_price * Decimal((100 - self.discount.value) / 100))
        else:
            return self.basket.total_price - (
                self.basket.total_price - self.discount.value)

    def get_status(self):
        return dict(Order.ORDER_STATUS.STATUS_CHOICES)[self.status]


class DiscountQuerySet(QuerySet):
    def get_active_discounts(self):
        now = timezone.now()
        return self.filter(available_from__lte=now, available_until__gte=now,
                           is_used=False)


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

    def mark_as_used(self):
        self.is_used = True

    def __str__(self):
        return '{} {}'.format(self.value, self.owner.username)


@receiver(post_save, sender=Order)
def on_order_save(sender, instance, created, **kwargs):
    if created and instance.discount:
        instance.discount.mark_as_used()
        instance.discount.save()


@receiver(post_save, sender=Order)
def send_email_to_customer(sender, instance, created, **kwargs):
    if created:
        send_email.delay(email=instance.basket.user.email)
