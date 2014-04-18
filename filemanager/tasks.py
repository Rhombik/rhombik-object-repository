from __future__ import absolute_import

#from exampleSettings.celery import app as celeryapp
from django.db import models
import os

from celery import Celery
from django.conf import settings


app = Celery('tasks',)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exampleSettings.settings')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task()
def zippedTask(project):
   from filemanager.models import zippedObjectProxy
   z = zippedObjectProxy(project=project)
   z.save()
   return


@app.task()
def thumbTask(self, fullfile):
   from thumbnailer import thumbnailer2

   self.filename, self.filetype = thumbnailer2.thumbnailify(fullfile, (self.filex, self.filey))
   #Bleh, this is awful. Means we won't have to refactor a bunch of other stuff, but implies some deeper architecture issues.
   if self.filetype=="text":
   #Means you won't get text files when you query thumobjects.
      self.filetype="norender"


   self.save(generate=False)
   return

