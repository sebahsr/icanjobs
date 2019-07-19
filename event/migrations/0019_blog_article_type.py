# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-19 06:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0018_auto_20190709_0948'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='article_type',
            field=models.IntegerField(choices=[(1, b'News Article'), (2, b'Blog Post')], default=1),
        ),
    ]
