# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-24 18:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breakdowns', '0049_auto_20180118_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialbreakdown',
            name='rate',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
    ]