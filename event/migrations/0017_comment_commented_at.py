# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-09 08:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0016_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='commented_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
