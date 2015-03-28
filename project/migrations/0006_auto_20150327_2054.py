# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_remove_project_valid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='body',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]
