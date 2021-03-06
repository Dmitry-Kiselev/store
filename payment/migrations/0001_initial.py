# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-19 08:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0003_auto_20170519_0805'),
    ]

    operations = [
        migrations.CreateModel(
            name='StripePayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('charge_id', models.CharField(max_length=32)),
                ('charged_sum', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount_sum', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.Order')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
