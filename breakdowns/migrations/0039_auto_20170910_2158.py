# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-10 21:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breakdowns', '0038_auto_20170910_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='duration',
            field=models.IntegerField(blank=True, help_text='Number of days of the package offering', null=True),
        ),
    ]
