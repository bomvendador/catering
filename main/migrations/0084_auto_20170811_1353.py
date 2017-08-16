# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-08-11 10:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0083_userpaymentdetails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phonenumber',
            name='user',
        ),
        migrations.RemoveField(
            model_name='useremail',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userpaymentdetails',
            name='user',
        ),
        migrations.AddField(
            model_name='phonenumber',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.PlaceContactPerson'),
        ),
        migrations.AddField(
            model_name='placecontactperson',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='useremail',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.PlaceContactPerson'),
        ),
        migrations.AddField(
            model_name='userpaymentdetails',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.PlaceContactPerson'),
        ),
    ]
