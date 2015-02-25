# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filemanager.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='fileobject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('subfolder', models.CharField(default=b'/', max_length=256)),
                ('filename', models.FileField(upload_to=filemanager.models.uploadpath)),
                ('filetype', models.CharField(default=b'norender', max_length=16, null=True, blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='htmlobject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body_rendered', models.TextField(null=True, verbose_name=b'Entry body as HTML', blank=True)),
                ('fileobject', models.ForeignKey(to='filemanager.fileobject', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='thumbobject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.FileField(null=True, upload_to=filemanager.models.uploadpath, blank=True)),
                ('filetype', models.CharField(max_length=16, null=True, blank=True)),
                ('filex', models.PositiveSmallIntegerField()),
                ('filey', models.PositiveSmallIntegerField()),
                ('fileobject', models.ForeignKey(to='filemanager.fileobject')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='zippedobject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.FileField(null=True, upload_to=b'projects/', blank=True)),
                ('project', models.ForeignKey(to='project.Project', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='thumbobject',
            unique_together=set([('filex', 'filey', 'fileobject')]),
        ),
    ]
