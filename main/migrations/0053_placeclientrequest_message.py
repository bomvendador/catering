# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-07-21 07:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0052_auto_20170721_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='placeclientrequest',
            name='message',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
