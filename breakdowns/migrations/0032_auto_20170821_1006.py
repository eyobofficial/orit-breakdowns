# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-21 10:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breakdowns', '0031_auto_20170821_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialbreakdown',
            name='rate',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12),
        ),
    ]
