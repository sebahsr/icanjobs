# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-28 13:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0048_auto_20190528_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobs.JobLevel'),
        ),
    ]
