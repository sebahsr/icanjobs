# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-26 01:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0006_auto_20190326_0105'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]