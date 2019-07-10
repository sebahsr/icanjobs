# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-09 06:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0051_auto_20190612_0941'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgeRange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startAge', models.IntegerField(verbose_name='Start Age')),
                ('endAge', models.IntegerField(verbose_name='Enda Age')),
            ],
        ),
        migrations.CreateModel(
            name='EmployerService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='JobSeekerService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='employement_status',
            field=models.IntegerField(blank=True, choices=[(1, b'Student'), (2, b'Fresh graduate'), (3, b'Unemployed'), (4, b'Employed Part-Time'), (5, b'Employed Full-Time')], null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='highest_education_level',
            field=models.IntegerField(blank=True, choices=[(1, b'TVET'), (2, b'Diploma'), (3, b"Bachelor's Degree"), (4, b'Graduate/Professional Degree')], null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='age',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='jobs.AgeRange'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.IntegerField(choices=[(1, 'Male'), (2, 'Female')], default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='job_types',
            field=models.ManyToManyField(related_name='jobseekers', to='jobs.JobType'),
        ),
        migrations.AddField(
            model_name='employee',
            name='services_intersted_in',
            field=models.ManyToManyField(related_name='jobseekers', to='jobs.JobSeekerService'),
        ),
    ]