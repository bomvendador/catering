# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-24 11:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_complexmenu_image_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='complexmenu',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
