# Generated by Django 2.1.7 on 2019-05-01 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bsyncviewer', '0002_auto_20190501_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='usecaseattribute',
            name='grouping_level',
            field=models.CharField(default='', max_length=500),
        ),
    ]