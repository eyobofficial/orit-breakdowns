# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-29 14:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('breakdowns', '0033_librarybreakdowncatagory_standardbreakdown_standardequipmentbreakdown_standardlabourbreakdown_standa'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_title', models.CharField(help_text='Title of Membership Account Type', max_length=120)),
                ('description', models.TextField(blank=True, help_text='Description of the account type. Example: packages, duration, etc', null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('duration', models.IntegerField(blank=True, help_text='Number of dates of the duration', null=True)),
            ],
            options={
                'ordering': ['full_title', 'price'],
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_title', models.CharField(help_text='Name of the Company', max_length=120)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Companies',
                'ordering': ['full_title'],
            },
        ),
        migrations.CreateModel(
            name='CompanyMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(help_text='Membership start date')),
                ('end_date', models.DateField(help_text='Membership end date')),
                ('company', models.ForeignKey(help_text='Title of the member Company', on_delete=django.db.models.deletion.CASCADE, to='breakdowns.Company')),
            ],
            options={
                'ordering': ['-end_date'],
            },
        ),
        migrations.CreateModel(
            name='UserMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(help_text='Membership start date')),
                ('end_date', models.DateField(help_text='Membership end date')),
                ('is_approved', models.BooleanField(default=False, help_text='Approve membership')),
                ('account_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='breakdowns.AccountType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-is_approved', '-end_date', 'account_type', 'user'],
            },
        ),
    ]
