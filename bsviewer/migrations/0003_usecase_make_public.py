# Generated by Django 2.1 on 2018-08-28 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bsviewer', '0002_usecase_schema'),
    ]

    operations = [
        migrations.AddField(
            model_name='usecase',
            name='make_public',
            field=models.BooleanField(default=False),
        ),
    ]
