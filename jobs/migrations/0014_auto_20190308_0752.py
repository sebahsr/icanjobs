# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-08 07:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0013_employeejobinterest_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeejobinterest',
            name='employement_type',
        ),
        migrations.AddField(
            model_name='employeejobinterest',
            name='employement_type',
            field=models.ManyToManyField(to='jobs.EmployementType'),
        ),
        migrations.RemoveField(
            model_name='employeejobinterest',
            name='job_region',
        ),
        migrations.AddField(
            model_name='employeejobinterest',
            name='job_region',
            field=models.ManyToManyField(to='jobs.Region'),
        ),
    ]
