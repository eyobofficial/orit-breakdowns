# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-04 12:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('breakdowns', '0025_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabourPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hourly_rate', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Current hourly rate', max_digits=12, null=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='breakdowns.City')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['city', 'hourly_rate'],
            },
        ),
        migrations.AlterModelOptions(
            name='labour',
            options={'ordering': ['full_title', '-updated_at']},
        ),
        migrations.AlterModelOptions(
            name='material',
            options={'ordering': ['full_title', '-updated_at']},
        ),
        migrations.RemoveField(
            model_name='labour',
            name='hourly_rate',
        ),
        migrations.RemoveField(
            model_name='material',
            name='rate',
        ),
        migrations.AddField(
            model_name='labourprice',
            name='labour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='breakdowns.Labour'),
        ),
    ]