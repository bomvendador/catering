# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-07-31 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0070_staff_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='add_info',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
