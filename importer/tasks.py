
import os
from celery import Celery, shared_task
from django.conf import settings

from jobtastic import JobtasticTask

from spider.spiders.thingiverse import runScraper



class ThingiUserTask(JobtasticTask):
    """
    The user want's all of thier things.
    """
    def calculate_results(self, urls, user):
        runScraper(urls, user=user)

class ThingiProjectTask(JobtasticTask):
    """
    Things are there, but users want them here. Lets go get them!
    In due time.
    """
    def calculate_results(self, urls, user):

        runScraper(urls, user=user)

class ThingiFileTask(JobtasticTast):
    '''Get an individual file... AND SAVE IT! AH HA HA HA!!!'''

app = Celery('tasks')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Settings.settings')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task()
def scrapeTask(urls, user):
        ThingiProjectTask().calculate_results(urls, user=user)
    #runScraper(urls, user=user)
