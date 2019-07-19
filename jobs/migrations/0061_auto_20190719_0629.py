# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-19 06:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0060_auto_20190710_0506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='end_month',
            field=models.CharField(choices=[(b'jan', b'January'), (b'feb', b'February'), (b'mar', b'March'), (b'apr', b'April'), (b'may', b'May'), (b'jun', b'June'), (b'jul', b'July'), (b'aug', b'August'), (b'sep', b'September'), (b'oct', b'October'), (b'nov', b'November'), (b'dec', b'December')], max_length=10),
        ),
        migrations.AlterField(
            model_name='education',
            name='start_month',
            field=models.CharField(choices=[(b'jan', b'January'), (b'feb', b'February'), (b'mar', b'March'), (b'apr', b'April'), (b'may', b'May'), (b'jun', b'June'), (b'jul', b'July'), (b'aug', b'August'), (b'sep', b'September'), (b'oct', b'October'), (b'nov', b'November'), (b'dec', b'December')], max_length=10),
        ),
        migrations.AlterField(
            model_name='experience',
            name='end_month',
            field=models.CharField(choices=[(b'jan', b'January'), (b'feb', b'February'), (b'mar', b'March'), (b'apr', b'April'), (b'may', b'May'), (b'jun', b'June'), (b'jul', b'July'), (b'aug', b'August'), (b'sep', b'September'), (b'oct', b'October'), (b'nov', b'November'), (b'dec', b'December')], max_length=10),
        ),
        migrations.AlterField(
            model_name='experience',
            name='start_month',
            field=models.CharField(choices=[(b'jan', b'January'), (b'feb', b'February'), (b'mar', b'March'), (b'apr', b'April'), (b'may', b'May'), (b'jun', b'June'), (b'jul', b'July'), (b'aug', b'August'), (b'sep', b'September'), (b'oct', b'October'), (b'nov', b'November'), (b'dec', b'December')], max_length=10),
        ),
    ]