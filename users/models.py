from django.contrib.auth.models import AbstractUser
from django.db import models

from order.models import Discount


class User(AbstractUser):
    address = models.CharField(max_length=120, verbose_name='Address')

    def has_discount(self):
        return self.discounts.get_active_discounts.exists()
