# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-02 17:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildingsync', '0011_buildingsyncattribute_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingsyncattribute',
            name='path',
            field=models.CharField(default='', max_length=250),
        ),
    ]
