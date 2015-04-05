from __future__ import absolute_import

import os

from celery import Celery

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Settings.settings')

import sys

#PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
#sys.path.append(PROJECT_PATH+"/../../lib/python2.7/site-packages/")
#sys.path.append(PROJECT_PATH+"/..")

app = Celery('tasks')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#print("Celery backend from exampleSettings.settings:  "+str(settings.CELERY_RESULT_BACKEND))

#@app.task(bind=True)
#def debug_task(self):
#    print('Request: {0!r}'.format(self.request))

