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

##This is the worst thing ever. I can't get it to run any real logic when a forighnkey gets deleted, so I suppose this will do.
@app.task()
def ThumbnailEnforcer():
   from project.models import Project
   z = Project.objects.filter(thumbnail__isnull=True, draft=False)
   for i in z:
       i.save()
   return

@app.task()
def ReadmeEnforcer():
   from project.models import Project
   z = Project.objects.filter(bodyfile__isnull=True, draft=False)
   #Search for things called "README.txt"

   #If no readme exists, create one using bodytext as template.

   return


