from __future__ import absolute_import

#from exampleSettings.celery import app as celeryapp
from django.db import models
import os

from celery import Celery
from django.conf import settings

from Settings.celery import app

##This is the worst thing ever. I can't get it to run any real logic when a forighnkey gets deleted, so I suppose this will do.
@app.task()
def fileEnforcer(item):
   from filemanager.models import fileobject
   from django.contrib.contenttypes.models import ContentType
   files = fileobject.objects.filter(object_id=item.id, content_type=ContentType.objects.get_for_model(item))
   for fileItem in files:
      fileItem.delete()
   return

@app.task()
def ReadmeEnforcer():
   from project.models import Project
   z = Project.objects.filter(bodyfile__isnull=True, draft=False)
   #Search for things called "README.txt"
   for i in z:
       i.draft = True
       i.save()
   return
   #If no readme exists, create one using bodytext as template.
