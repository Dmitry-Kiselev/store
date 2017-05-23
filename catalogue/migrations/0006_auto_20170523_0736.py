# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-23 07:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0005_productrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productrating',
            name='rated_product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='catalogue.Product'),
        ),
        migrations.AlterField(
            model_name='productrating',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]