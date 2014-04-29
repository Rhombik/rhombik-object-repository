from __future__ import absolute_import

#from exampleSettings.celery import app as celeryapp
from django.db import models
import os

from celery import Celery, shared_task
from django.conf import settings

app = Celery('tasks',)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Settings.settings')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task()
def zippedTask(project):
   from filemanager.models import zippedObjectProxy
   z = zippedObjectProxy(project=project)
   z.save()
   return


@app.task()
def thumbTask(thumbnailpk, fullfilepk):
   from thumbnailer import thumbnailer2
   from filemanager.models import fileobject, thumbobject
   print(app)
   #Celery pickles the object before it sends it to the queue, so we need to look it up on this side.
   thumbnail= thumbobject.objects.get(pk=thumbnailpk)
   fullfile = fileobject.objects.get(pk=fullfilepk)

   print(thumbnail)
   print(fullfile)

   thumbnail.filename, thumbnail.filetype = thumbnailer2.thumbnailify(fullfile, (thumbnail.filex, thumbnail.filey))
   #Bleh, this is awful. Means we won't have to refactor a bunch of other stuff, but implies some deeper architecture issues.
   if thumbnail.filetype=="text":
   #Means you won't get text files when you query thumobjects.
      thumbnail.filetype="norender"
   if thumbnail.filename:
       thumbnail.save(generate=False)
   else:
       import time
       time.sleep(5)
       thumbTask.delay(self, fullfile)
   return

