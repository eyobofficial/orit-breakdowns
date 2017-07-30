# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-22 19:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breakdowns', '0008_auto_20170722_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='costbreakdown',
            name='output',
            field=models.DecimalField(decimal_places=2, default=3, help_text='Labour and equipment output', max_digits=3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='costbreakdown',
            name='overhead',
            field=models.DecimalField(decimal_places=2, help_text='Overhead percentage in decimal number. Example: 0.15 for 15%', max_digits=6),
        ),
        migrations.AlterField(
            model_name='costbreakdown',
            name='profit',
            field=models.DecimalField(decimal_places=2, help_text='Profit percentage in decimal number. Example: 0.2 for 20%', max_digits=6),
        ),
    ]
