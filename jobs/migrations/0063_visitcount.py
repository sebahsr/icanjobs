# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-30 08:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0062_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniqueHitCount', models.IntegerField()),
                ('totalHitCount', models.IntegerField()),
            ],
        ),
    ]
