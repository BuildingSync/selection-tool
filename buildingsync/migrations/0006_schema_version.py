# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-04-27 14:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('buildingsync', '0005_buildingsyncattribute_tree_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='schema',
            name='version',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
