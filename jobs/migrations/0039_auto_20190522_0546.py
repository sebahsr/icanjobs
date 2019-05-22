# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-22 05:46
from __future__ import unicode_literals

from django.db import migrations, models
import jobs.functions


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0038_auto_20190521_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='profile_pic',
            field=models.FileField(blank=True, default='test.jpg', upload_to=jobs.functions.getFileName),
            preserve_default=False,
        ),
    ]
