# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-10 22:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('breakdowns', '0041_companymembership_registered_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermembership',
            name='registered_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
