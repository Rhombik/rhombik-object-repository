# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=60, unique=True, null=True, blank=True)),
                ('body', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('allow_html', models.BooleanField(default=False)),
                ('draft', models.BooleanField(default=False)),
                ('valid', models.BooleanField(default=False)),
                ('ratingSortBest', models.FloatField(default=1)),
                ('ratingCount', models.IntegerField(null=True, blank=True)),
                ('rating_votes', models.PositiveIntegerField(default=0, editable=False, blank=True)),
                ('rating_score', models.IntegerField(default=0, editable=False, blank=True)),
                ('downloadcount_votes', models.PositiveIntegerField(default=0, editable=False, blank=True)),
                ('downloadcount_score', models.IntegerField(default=0, editable=False, blank=True)),
                ('author', models.ForeignKey(related_name='author', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
