# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-19 11:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conf', '0002_auto_20170517_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfig',
            name='address_lat',
            field=models.FloatField(blank=True, null=True, verbose_name='Latitude'),
        ),
        migrations.AddField(
            model_name='siteconfig',
            name='address_lng',
            field=models.FloatField(blank=True, null=True, verbose_name='Longitude'),
        ),
    ]
