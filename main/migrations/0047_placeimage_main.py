# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-07-20 10:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0046_auto_20170720_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='placeimage',
            name='main',
            field=models.BooleanField(default=False),
        ),
    ]
