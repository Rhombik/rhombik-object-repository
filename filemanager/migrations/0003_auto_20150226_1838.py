# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filemanager.models


class Migration(migrations.Migration):

    dependencies = [
        ('filemanager', '0002_auto_20150222_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileobject',
            name='filename',
            field=models.FileField(upload_to=filemanager.models.fileuploadpath),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thumbobject',
            name='filename',
            field=models.FileField(null=True, upload_to=filemanager.models.thumbuploadpath, blank=True),
            preserve_default=True,
        ),
    ]
