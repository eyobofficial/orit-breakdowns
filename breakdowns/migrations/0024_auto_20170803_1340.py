# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-03 13:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('breakdowns', '0023_auto_20170803_1215'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, help_text="Supplier's current material price(Before TAX)", max_digits=12)),
                ('updated_at', models.DateField(auto_now=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='breakdowns.Material')),
            ],
            options={
                'ordering': ['material', '-price'],
            },
        ),
        migrations.CreateModel(
            name='MaterialSupplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_title', models.CharField(help_text='Material Supplier Company name', max_length=120)),
                ('short_title', models.CharField(blank=True, help_text='Material Supplier short(unofficial) name', max_length=30, null=True)),
                ('description', models.TextField(blank=True, help_text='Short summary about the supplier', null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['full_title'],
            },
        ),
        migrations.AddField(
            model_name='materialprice',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='breakdowns.MaterialSupplier'),
        ),
    ]