# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

class Migration(migrations.Migration):

    dependencies = [
        ('filemanager', '0004_auto_20150327_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zippedobject',
            name='filename',
            field=models.FileField(upload_to=b'projects/'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='zippedobject',
            name='project',
            field=models.ForeignKey(to='project.Project'),
            preserve_default=True,
        ),
    ]
