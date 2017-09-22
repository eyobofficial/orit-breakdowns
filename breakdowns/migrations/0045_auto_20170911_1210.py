# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-11 12:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breakdowns', '0044_package_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='level',
            field=models.IntegerField(help_text='Level of the membership packages', unique=True),
        ),
    ]
