# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filemanager.models


class Migration(migrations.Migration):

    dependencies = [
        ('filemanager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thumbobject',
            name='filename',
            field=models.FileField(null=True, upload_to=filemanager.models.uploadpath, blank=True),
            preserve_default=True,
        ),
    ]
