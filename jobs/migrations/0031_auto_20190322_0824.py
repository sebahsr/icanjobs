# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-22 08:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0030_auto_20190314_1408'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Sector', 'verbose_name_plural': 'Sectors'},
        ),
    ]
