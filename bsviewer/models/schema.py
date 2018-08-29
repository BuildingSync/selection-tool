import os
import csv

from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from bsviewer.lib.schema_parser import process_schema


def rename_schema_file(instance, path):
    if instance.version:
        return '{}buildingsync_v_{}.xsd'.format('uploaded_schemas/',
                                                instance.version.replace('.', '_'))
    else:
        pass


# BuildingSync Schema versions


class Schema(models.Model):
    name = models.CharField(max_length=100, default="0.3.0", unique=True)
    version = models.CharField(max_length=100, default="0.3", unique=True, null=False)
    schema_file = models.FileField(upload_to=rename_schema_file)
    schema_parsed = models.BooleanField(default=False)
    mapping_template_file = models.FileField(upload_to='mapping/templates/')

    def __str__(self):
        return self.name

    def save_template(self):
        '''
        Generate the use case template

        :return: list, CSV format
        '''
        required_paths = ['Audits.Audit']

        data = [['BuildingSync Path', 'Ignored (Blank), Optional, Required']]
        for attribute in self.attributes.all().order_by('index'):
            print(attribute.index)
            if attribute.path in required_paths:
                data.append([attribute.path, 'Required'])
            else:
                data.append([attribute.path, ''])

        tmp_file = 'mapping_template_%s.csv' % self.version
        with open(tmp_file, 'w', newline='') as f:
            wr = csv.writer(f)
            wr.writerows(data)

        self.mapping_template_file = tmp_file

        return tmp_file


@receiver(post_save, sender=Schema)
def parse_schema(sender, instance, **kwargs):
    # TODO: if parsed bool is false, call 'parse' function in schema_parser
    # set 'parsed' bool to True on Schema model and save
    print('SCHEMA PARSED? {}'.format(instance.schema_parsed))
    if instance.schema_parsed is False:
        process_schema(instance)
        # set parsed = true so it doesn't get parsed again
        instance.schema_parsed = True
        instance.save()


# These two auto-delete files from filesystem when they are unneeded:

@receiver(post_delete, sender=Schema)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Schema` object is deleted.
    """
    if instance.schema_file:
        if os.path.isfile(instance.schema_file.path):
            os.remove(instance.schema_file.path)


@receiver(pre_save, sender=Schema)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Schema.objects.get(pk=instance.pk).schema_file
    except Schema.DoesNotExist:
        return False

    new_file = instance.schema_file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
