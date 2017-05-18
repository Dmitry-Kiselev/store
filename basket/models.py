from django.conf import settings
from django.db import models

from catalogue.models import Product
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    is_submitted = models.BooleanField(default=False)

    def __str__(self):
        return 'Basket {}'.format(self.user.username)

    @property
    def total_price(self):
        return sum([line.line_price for line in self.lines.all()])

    def total_price_inc_discount(self):
        if not self.user.has_discount():
            return self.total_price

        discount = self.user.get_discount()

        if discount.in_percent:
            return self.total_price * ((100 - discount.value) / 100)
        else:
            return self.total_price - discount.value

    def all_lines(self):
        return self.lines.all()


class Line(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE,
                               related_name='lines')

    @property
    def line_price(self):
        return self.product.price * self.quantity


@receiver(post_save, sender=Line)
def update_lines_count_in_cache_on_save(sender, instance, created, **kwargs):
    count = instance.basket.all_lines().count()
    cache.set('basket_%s' % instance.basket.pk,
              count, None)


@receiver(post_delete, sender=Line)
def update_lines_count_in_cache_on_delete(sender, instance, **kwargs):
    count = instance.basket.all_lines().count()
    cache.set('basket_%s' % instance.basket.pk,
              count, None)
