
import os
from celery import Celery, shared_task
from django.conf import settings

from jobtastic import JobtasticTask

from spider.spiders.thingiverse import runScraper

class Thingitask(JobtasticTask):
    """
    Things are there, but users want them here. Lets go get them!
    In due time.
    """
    def calculate_results(self, urls, user):
        runScraper(urls, user=user)
class add(JobtasticTask):
    """
    peanuts are good, when you want a simple food.
    """
    def calculate_results(self, x,y):
        return(x+y)


app = Celery('tasks')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Settings.settings')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task()
def scrapeTask(urls, user):
    Thingitask().calculate_results(urls, user=user)
    #runScraper(urls, user=user)
