from django.db import models

from solo.models import SingletonModel


class SiteConfig(SingletonModel):
    class Meta:
        verbose_name = 'Site configuration'

    company_name = models.CharField(max_length=30, blank=True, null=True)
    company_description = models.TextField(verbose_name='Description',
                                           blank=True, null=True)
    open_time = models.TimeField(blank=True, null=True)
    close_time = models.TimeField(blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    address_lat = models.FloatField(verbose_name='Latitude', blank=True,
                                    null=True)
    address_lng = models.FloatField(verbose_name='Longitude', blank=True,
                                    null=True)
    fixed_shipping_price = models.DecimalField(max_digits=6, decimal_places=2,
                                               default=30.0)
    shipping_price_per_km = models.DecimalField(max_digits=5, decimal_places=2,
                                                default=1.5)  # if user set location on map
    free_shipping_on = models.DecimalField(max_digits=5, decimal_places=2,
                                           default=150.0,
                                           help_text='Provide free shipping for orders with certain total price')
    admin_email = models.EmailField(
        verbose_name='email to send notification about some problems with website',
        blank=True, null=True)
