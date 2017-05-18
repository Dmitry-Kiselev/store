from django.contrib.auth.models import AbstractUser
from django.db import models

from basket.models import Basket
from order.models import Discount


class User(AbstractUser):
    address = models.CharField(max_length=120, verbose_name='Address')

    def has_discount(self):
        return self.discounts.get_active_discounts().exists()

    def get_discount(self):
        return self.discounts.get_active_discounts().first()

    @property
    def basket(self):
        basket, created = Basket.objects.get_or_create(user=self,
                                                       is_submitted=False)
        return basket
