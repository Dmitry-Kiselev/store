# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-17 06:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=30)),
                ('company_description', models.TextField(verbose_name='Description')),
                ('open_time', models.TimeField()),
                ('close_time', models.TimeField()),
                ('address', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Site configuration',
            },
        ),
    ]