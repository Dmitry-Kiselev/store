# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-19 11:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conf', '0004_auto_20170519_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfig',
            name='free_shipping_on',
            field=models.DecimalField(decimal_places=2, default=150.0, help_text='Provide free shipping for orders with certain total price', max_digits=5),
        ),
    ]