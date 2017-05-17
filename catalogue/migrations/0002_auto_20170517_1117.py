# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-17 11:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timestampedmodel',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='timestampedmodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]