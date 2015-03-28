# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filemanager.models


def deleteDeadFiles(apps, schema_editor):
    fileObject = apps.get_model("filemanager", "fileObject")
    files = fileObject.objects.all()
    for fileInstance in files:
        if not fileInstance.filename:
            fileInstance.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('filemanager', '0003_auto_20150226_1838'),
    ]

    operations = [
        migrations.RunPython(deleteDeadFiles),
        migrations.AlterField(
            model_name='thumbobject',
            name='filename',
            field=models.FileField(upload_to=filemanager.models.thumbuploadpath),
            preserve_default=True,
        ),
    ]
