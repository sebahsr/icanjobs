# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-06 23:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jobs.functions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('profile_pic', models.FileField(upload_to=jobs.functions.getFileName)),
                ('brief_description', models.TextField()),
                ('country', models.CharField(choices=[(b'ET', b'Ethopia'), (b'ER', b'Eritrea')], max_length=10)),
                ('website', models.URLField()),
                ('phone', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('profile_pic', models.FileField(upload_to=jobs.functions.getFileName)),
                ('age', models.IntegerField()),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('city', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmployementType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('summary', models.TextField()),
                ('requirements', models.TextField()),
                ('salary', models.FloatField(default=0)),
                ('position', models.CharField(max_length=100)),
                ('number_of_candidates', models.IntegerField(default=0)),
                ('deadline', models.DateTimeField()),
                ('status', models.IntegerField(choices=[(1, b'Opened'), (2, b'Closed')])),
                ('city', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('views', models.IntegerField()),
                ('categories', models.ManyToManyField(related_name='jobs', to='jobs.Category')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Company')),
                ('employement_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.EmployementType')),
            ],
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Pe', 'Pending'), ('Ac', 'Accepted'), ('Re', 'Rejected')], max_length=10)),
                ('applied_on', models.DateTimeField(auto_now_add=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Employee')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Job')),
            ],
        ),
        migrations.CreateModel(
            name='JobLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.JobLevel'),
        ),
        migrations.AddField(
            model_name='job',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Region'),
        ),
        migrations.AddField(
            model_name='employee',
            name='applications',
            field=models.ManyToManyField(related_name='applicants', through='jobs.JobApplication', to='jobs.Job'),
        ),
        migrations.AddField(
            model_name='employee',
            name='intersted_in',
            field=models.ManyToManyField(to='jobs.Category'),
        ),
        migrations.AddField(
            model_name='employee',
            name='regiion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Region'),
        ),
        migrations.AddField(
            model_name='employee',
            name='school_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.SchoolLevel'),
        ),
    ]
