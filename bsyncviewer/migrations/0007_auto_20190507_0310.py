# Generated by Django 2.1.7 on 2019-05-07 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bsyncviewer', '0006_auto_20190506_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usecaseattribute',
            name='grouping_level',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
