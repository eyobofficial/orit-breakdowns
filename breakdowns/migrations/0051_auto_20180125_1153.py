# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-25 11:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breakdowns', '0050_auto_20180124_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labourbreakdown',
            name='hourly_rate',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
    ]
