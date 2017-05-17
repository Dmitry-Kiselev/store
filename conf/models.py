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
