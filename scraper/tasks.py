
import os
from celery import Celery, shared_task
from django.conf import settings

from spider.spiders.thingiverse import runScraper

app = Celery('tasks')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Settings.settings')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task()
def scrapeTask(urls, user):
    runScraper(urls, user=user)
