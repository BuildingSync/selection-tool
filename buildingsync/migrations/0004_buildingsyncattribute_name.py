# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-04-27 04:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('buildingsync', '0003_buildingsyncattribute'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingsyncattribute',
            name='name',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
    ]
