# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-24 10:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_auto_20170423_0126'),
    ]

    operations = [
        migrations.AddField(
            model_name='complexmenu',
            name='image_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
