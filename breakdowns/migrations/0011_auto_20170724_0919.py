# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 09:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breakdowns', '0010_auto_20170724_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialbreakdown',
            name='rate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]
