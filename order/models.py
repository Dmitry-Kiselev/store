from django.db import models
from django.db.models import QuerySet

from basket.models import Basket
from catalogue.models import TimeStampedModel
from django.utils import timezone


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


class DiscountQuerySet(QuerySet):
    def get_active_discounts(self):
        now = timezone.now()
        return self.filter(available_from__gte=now, available_until__lte=now)


class Discount(models.Model):
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE,
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
