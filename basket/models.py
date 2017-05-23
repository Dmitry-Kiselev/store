import traceback
from decimal import Decimal

import logging
from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from redis.exceptions import ConnectionError

from catalogue.models import Product
from conf.models import SiteConfig

logger = logging.getLogger('django')


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    is_submitted = models.BooleanField(default=False)

    def __str__(self):
        return 'Basket {}'.format(self.user.username)

    @property
    def total_price(self):
        return sum([line.line_price for line in self.lines.all()])

    @property
    def total_price_inc_discount(self):
        if not self.user.has_discount():
            return self.total_price

        discount = self.user.get_discount()

        if discount.in_percent:
            price = self.total_price * ((100 - discount.value) / 100)
            return price if price >= 0 else 0
        else:
            price = self.total_price - discount.value
            return price if price >= 0 else 0

    def submit(self):
        self.is_submitted = True

    def all_lines(self):
        return self.lines.all()

    @property
    def shipping_price(self):
        conf = SiteConfig.get_solo()
        if self.total_price_inc_discount > conf.free_shipping_on:
            return 0  # free shipping

        distance = self.user.distance
        if distance is None:
            return conf.fixed_shipping_price  # fixed price

        return Decimal(distance) * conf.shipping_price_per_km

    @property
    def total_incl_discount_incl_shipping(self):
        return self.total_price_inc_discount + self.shipping_price


class Line(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE,
                               related_name='lines')

    @property
    def line_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return '{} {}'.format(self.product.name, self.quantity)


@receiver(post_delete, sender=Line)
@receiver(post_save, sender=Line)
def update_lines_count_in_cache(sender, instance, created=None, **kwargs):
    count = instance.basket.all_lines().count()
    try:
        cache.set('basket_{}'.format(instance.basket.pk),
                  count, None)
    except ConnectionError as e:
        logger.error('{} {}: {}'.format(timezone.now(), str(e),
                                        traceback.format_exc()))
