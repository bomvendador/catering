# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-17 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_ingredients_ingredientsformeal'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredients',
            name='icon',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
