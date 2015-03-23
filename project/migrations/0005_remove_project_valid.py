# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20150303_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='valid',
        ),
    ]
