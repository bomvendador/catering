# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-07-21 08:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0054_auto_20170721_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientrequest',
            name='place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Place'),
        ),
    ]
