# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-25 22:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_complexmenubydate_menu_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='mealforcomplexmenu',
            name='menu_by_date',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.ComplexMenuByDate'),
        ),
    ]
