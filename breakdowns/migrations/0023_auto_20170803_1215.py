# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-03 12:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('breakdowns', '0022_auto_20170801_1632'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitCatagory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_title', models.CharField(max_length=60)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['full_title'],
            },
        ),
        migrations.AddField(
            model_name='unit',
            name='catagory',
            field=models.ForeignKey(default=1, help_text='Type of measurement units', on_delete=django.db.models.deletion.CASCADE, to='breakdowns.UnitCatagory'),
            preserve_default=False,
        ),
    ]
