# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-07 15:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0007_auto_20190307_1504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='email',
        ),
    ]
