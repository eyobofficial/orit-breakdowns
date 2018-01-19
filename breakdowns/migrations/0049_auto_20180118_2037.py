# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-18 20:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breakdowns', '0048_auto_20180118_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='costbreakdown',
            name='overhead',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Example: Enter 15 for 15% Overhead', max_digits=6, null=True, verbose_name='Overhead (%)'),
        ),
        migrations.AlterField(
            model_name='costbreakdown',
            name='profit',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Example: Enter 25 for 25% Profit', max_digits=6, null=True, verbose_name='Profit (%)'),
        ),
    ]