# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-19 09:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0020_auto_20190719_0931'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertisement',
            old_name='title',
            new_name='description',
        ),
    ]
