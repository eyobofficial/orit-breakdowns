# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-29 11:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('breakdowns', '0032_auto_20170821_1006'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryBreakdownCatagory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_title', models.CharField(help_text='Work type catagory for breakdown', max_length=120)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Cost Breakdown Catagories',
                'ordering': ['full_title'],
            },
        ),
        migrations.CreateModel(
            name='StandardBreakdown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_title', models.CharField(help_text='Work Item Title', max_length=120)),
                ('description', models.TextField(blank=True, null=True)),
                ('output', models.DecimalField(decimal_places=2, help_text='Labour and equipment output', max_digits=3)),
                ('updated_at', models.DateField(auto_now=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('library_breakdown_catagory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='breakdowns.LibraryBreakdownCatagory')),
                ('unit', models.ForeignKey(help_text='Measurement unit for the breakdown', on_delete=django.db.models.deletion.CASCADE, to='breakdowns.Unit')),
            ],
            options={
                'verbose_name_plural': 'Standard library breakdowns',
                'verbose_name': 'Standard library breakdown',
                'permissions': (('manage_library', 'Can manage standard breakdown library'),),
                'ordering': ['full_title', '-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='StandardEquipmentBreakdown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=1)),
                ('uf', models.DecimalField(decimal_places=2, default=1, max_digits=3)),
                ('updated_at', models.DateField(auto_now=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='breakdowns.Equipment')),
                ('standard_breakdown', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='breakdowns.StandardBreakdown')),
            ],
            options={
                'verbose_name_plural': 'standard equipment breakdowns',
                'verbose_name': 'standard equipment breakdown',
                'ordering': ['standard_breakdown', 'equipment', '-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='StandardLabourBreakdown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=1)),
                ('uf', models.DecimalField(decimal_places=2, default=1, max_digits=3)),
                ('updated_at', models.DateField(auto_now=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('labour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='breakdowns.Labour')),
                ('standard_breakdown', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='breakdowns.StandardBreakdown')),
            ],
            options={
                'verbose_name_plural': 'standard labour breakdowns',
                'verbose_name': 'standard labour breakdown',
                'ordering': ['standard_breakdown', 'labour', '-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='StandardLibrary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_title', models.CharField(help_text='Title of the standard library', max_length=120)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Standard Libraries',
                'verbose_name': 'Standard Library',
                'ordering': ['full_title'],
            },
        ),
        migrations.CreateModel(
            name='StandardMaterialBreakdown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, default=1, max_digits=12)),
                ('updated_at', models.DateField(auto_now=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='breakdowns.Material')),
                ('standard_breakdown', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='breakdowns.StandardBreakdown')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='breakdowns.Unit')),
            ],
            options={
                'verbose_name_plural': 'standard material breakdowns',
                'verbose_name': 'standard material breakdown',
                'ordering': ['standard_breakdown', 'material', '-updated_at'],
            },
        ),
    ]