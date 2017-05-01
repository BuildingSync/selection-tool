# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-04-27 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildingsync', '0006_schema_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingsyncattribute',
            name='index',
            field=models.IntegerField(default=0, verbose_name='For a given schema, this is the index in the linear tree list'),
        ),
    ]