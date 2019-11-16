# Generated by Django 2.1 on 2018-12-06 17:39

import bsyncviewer.models.schema
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=250)),
                ('type', models.CharField(default='<unknown_type>', max_length=100)),
                ('parent', models.CharField(max_length=250, null=True)),
                ('tree_level', models.IntegerField()),
                ('path', models.CharField(default='', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeEnumerationClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bsyncviewer.Attribute')),
            ],
        ),
        migrations.CreateModel(
            name='BedesEnumeration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_uuid', models.CharField(max_length=100, unique=True)),
                ('term', models.CharField(max_length=100, unique=True)),
                ('url', models.CharField(max_length=300)),
                ('definition', models.TextField(blank=True, null=True)),
                ('related_term_uuid', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BedesEnumerationMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bedesEnumeration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bsyncviewer.BedesEnumeration')),
            ],
        ),
        migrations.CreateModel(
            name='BedesMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bsyncviewer.Attribute')),
            ],
        ),
        migrations.CreateModel(
            name='BedesTerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_uuid', models.CharField(max_length=100, unique=True)),
                ('term', models.CharField(max_length=100, unique=True)),
                ('category', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=300)),
                ('definition', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Enumeration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='EnumerationClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='0.3.0', max_length=100, unique=True)),
                ('version', models.CharField(default='0.3.0', max_length=100, unique=True)),
                ('schema_file', models.FileField(null=True, upload_to=bsyncviewer.models.schema.rename_schema_file)),
                ('schema_parsed', models.BooleanField(default=False, help_text='Leave blank. This will be auto-populated.')),
                ('usecase_template_file', models.FileField(blank=True, help_text='Leave blank. This will be auto-populated.', null=True, upload_to='usecase_templates/')),
            ],
        ),
        migrations.CreateModel(
            name='UseCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Use Case Name', max_length=100)),
                ('description', models.TextField()),
                ('make_public', models.BooleanField(default=False)),
                ('import_file', models.FileField(blank=True, null=True, upload_to='usecase_mappings/')),
                ('usecase_parsed', models.BooleanField(default=False)),
                ('parsing_errors', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), blank=True, null=True, size=None)),
            ],
        ),
        migrations.CreateModel(
            name='UseCaseAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(choices=[(0, 'Ignored'), (1, 'Optional'), (2, 'Required')], default=0)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bsyncviewer.Attribute')),
                ('use_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bsyncviewer.UseCase')),
            ],
        ),
        migrations.CreateModel(
            name='UseCaseEnumeration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(choices=[(0, 'Ignored'), (1, 'Optional'), (2, 'Required')], default=0)),
                ('enumeration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bsyncviewer.Enumeration')),
                ('use_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bsyncviewer.UseCase')),
            ],
        ),
        migrations.CreateModel(
            name='UseCaseUDF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(choices=[(0, 'Ignored'), (1, 'Optional'), (2, 'Required')], default=0)),
                ('values', models.CharField(max_length=512)),
                ('associated_field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bsyncviewer.UseCaseUDF')),
                ('use_case_attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bsyncviewer.UseCaseAttribute')),
            ],
        ),
        migrations.AddField(
            model_name='usecase',
            name='attributes',
            field=models.ManyToManyField(related_name='usecaseattributes', through='bsyncviewer.UseCaseAttribute', to='bsyncviewer.Attribute'),
        ),
        migrations.AddField(
            model_name='usecase',
            name='enumerations',
            field=models.ManyToManyField(through='bsyncviewer.UseCaseEnumeration', to='bsyncviewer.Enumeration'),
        ),
        migrations.AddField(
            model_name='usecase',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usecase',
            name='schema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bsyncviewer.Schema'),
        ),
        migrations.AddField(
            model_name='enumerationclass',
            name='schema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bsyncviewer.Schema'),
        ),
        migrations.AddField(
            model_name='enumeration',
            name='enumeration_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enumerations', to='bsyncviewer.EnumerationClass'),
        ),
        migrations.AddField(
            model_name='enumeration',
            name='schema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enumerations', to='bsyncviewer.Schema'),
        ),
        migrations.AddField(
            model_name='bedesmapping',
            name='bedesTerm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bsyncviewer.BedesTerm'),
        ),
        migrations.AddField(
            model_name='bedesenumerationmapping',
            name='enumeration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bsyncviewer.Enumeration'),
        ),
        migrations.AddField(
            model_name='attributeenumerationclass',
            name='enumeration_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bsyncviewer.EnumerationClass'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='enumeration_classes',
            field=models.ManyToManyField(through='bsyncviewer.AttributeEnumerationClass', to='bsyncviewer.EnumerationClass'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='schema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='bsyncviewer.Schema'),
        ),
        migrations.AlterUniqueTogether(
            name='usecaseenumeration',
            unique_together={('enumeration', 'use_case')},
        ),
        migrations.AlterUniqueTogether(
            name='usecaseattribute',
            unique_together={('attribute', 'use_case')},
        ),
    ]
