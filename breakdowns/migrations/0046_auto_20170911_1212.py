# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-11 12:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('breakdowns', '0045_auto_20170911_1210'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ['full_title'], 'verbose_name_plural': 'Cities'},
        ),
    ]
