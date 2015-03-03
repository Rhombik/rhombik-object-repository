# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20150226_1838'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': (('view', 'View'), ('edit', 'Edit'))},
        ),
    ]
