from __future__ import absolute_import

#from exampleSettings.celery import app as celeryapp
from django.db import models
import os

from celery import Celery, shared_task
from django.conf import settings

from django.core.files.uploadedfile import UploadedFile
from io import BytesIO
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from project.models import Project

app = Celery('tasks')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Settings.settings')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task()
def zippedTask(project):
   from filemanager.models import zippedobject,fileobject
   import zipfile
   from django.core.files.base import ContentFile
   s = BytesIO()

   data = zipfile.ZipFile(s,'a')
   object_type = ContentType.objects.get_for_model(project)
   projectfiles = fileobject.objects.filter(content_type=object_type,object_id=project.id)
   for filedata in projectfiles:
       filed = filedata.filename.read()
       pathAndName = str(project.title)+filedata.subfolder+os.path.split(str(filedata.filename))[1] #### this is where subfolders will be added to inside the zip file.
       data.writestr(pathAndName, filed)
   data.close()
   s.seek(0)
   filedata = ContentFile(s.getvalue())
   filedata.name = project.title+".zip"
   zippedobject.create(filename = filedata)

#def thumbsave(thumbnail):
#   import time
#   print(str(thumbnail)+" thumbsave class")
#   if thumbnail.filename:
#        thumbnail.save(generate=False)
#   else:
#       time.sleep(1)
#       thumbsave(thumbnail)


@app.task()
def thumbTask(thumbnail, fullfile):
   from thumbnailer import thumbnailer2
   from filemanager.models import fileobject, thumbobject
   thumbnail.filename, thumbnail.filetype = thumbnailer2.thumbnailify(fullfile, (thumbnail.filex, thumbnail.filey))
   #Bleh, this is awful. Means we won't have to refactor a bunch of other stuff, but implies some deeper architecture issues.
   if thumbnail.filetype=="text" or thumbnail.filetype=="" or thumbnail.filetype=="norender":
      thumbnail.filetype="norender"
      thumbnail.filename = None
   thumbnail.save(generate=False)


