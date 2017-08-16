# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-26 19:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_cartmeals_menu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartmeals',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Cart'),
        ),
        migrations.AlterField(
            model_name='cartmeals',
            name='meal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Meal'),
        ),
    ]
