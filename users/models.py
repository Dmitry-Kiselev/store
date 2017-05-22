from math import sin, cos, sqrt, atan2, radians

from django.contrib.auth.models import AbstractUser
from django.db import models

from basket.models import Basket
from conf.models import SiteConfig
from order.models import Discount


class User(AbstractUser):
    address = models.CharField(max_length=120, verbose_name='Address')
    address_lat = models.FloatField(verbose_name='Latitude', blank=True,
                                    null=True)
    address_lng = models.FloatField(verbose_name='Longitude', blank=True,
                                    null=True)

    def has_discount(self):
        return self.discounts.get_active_discounts().exists()

    def get_discount(self):
        return self.discounts.get_active_discounts().first()

    @property
    def basket(self):
        basket, created = Basket.objects.get_or_create(user=self,
                                                       is_submitted=False)
        return basket

    @property
    def distance(self):
        conf = SiteConfig.get_solo()
        company_lat, company_lng = conf.address_lat, conf.address_lng
        user_lat, user_lng = self.address_lat, self.address_lng

        if not (company_lat and company_lng and user_lat and user_lng):
            return None

        # approximate radius of earth in km
        R = 6373.0

        lat1 = radians(company_lat)
        lon1 = radians(company_lng)
        lat2 = radians(user_lat)
        lon2 = radians(user_lng)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        return distance
