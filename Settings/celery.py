from __future__ import absolute_import

import os
import django

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Settings.settings')
#django.setup()

app = Celery('tasks')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

#import sys

#PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
#sys.path.append(PROJECT_PATH+"/../../lib/python2.7/site-packages/")
#sys.path.append(PROJECT_PATH+"/..")
