from django.db import models

from solo.models import SingletonModel


class SiteConfig(SingletonModel):
    class Meta:
        verbose_name = 'Site configuration'

    company_name = models.CharField(max_length=30)
    company_description = models.TextField(verbose_name='Description')
    open_time = models.TimeField()
    close_time = models.TimeField()
    address = models.CharField(max_length=50)
