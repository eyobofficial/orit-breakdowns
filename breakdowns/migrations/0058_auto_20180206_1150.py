# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-06 11:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('breakdowns', '0057_auto_20180127_1720'),
    ]

    operations = [
        migrations.CreateModel(
            name='FreelanceUserSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deactivate', models.BooleanField(default=False, verbose_name='Deactivate Account')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_title', models.CharField(max_length=120, verbose_name='Plan Full Title')),
                ('short_title', models.CharField(blank=True, max_length=60, null=True, verbose_name='Plan Short Title')),
                ('is_premium', models.BooleanField(default=False)),
                ('is_default', models.BooleanField(default=False)),
                ('duration', models.IntegerField(blank=True, help_text='Duration in calendar days', null=True, verbose_name='Plan Duration')),
                ('price_per_year', models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Annual Subscription Fee')),
                ('no_of_projects', models.IntegerField(help_text='Number of projects a user can create')),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['is_default', 'is_premium', 'price_per_year', 'full_title'],
            },
        ),
        migrations.AddField(
            model_name='freelanceusersubscription',
            name='user_plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='breakdowns.UserPlan'),
        ),
    ]
