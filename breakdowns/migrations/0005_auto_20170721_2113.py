# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-21 21:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('breakdowns', '0004_auto_20170721_0736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='equipment_catagory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='breakdowns.EquipmentCatagory'),
        ),
    ]
