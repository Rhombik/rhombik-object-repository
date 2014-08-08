from django.db import models
from haystack import signals
from celery import Celery, shared_task
import os
from project.search_indexes import ProjectIndex
from haystack.query import SearchQuerySet

app = Celery('tasks')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Settings.settings')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


class celerySignalProcessor(signals.RealtimeSignalProcessor):
    def handle_save(self, sender, instance, **kwargs):
        if str(sender) == "<class 'project.models.Project'>" and instance.draft == False:
            reindex_mymodel.delay(sender, instance)
        elif str(sender) == "<class 'project.models.Project'>" and instance.draft == True:
            pass
        else:
            super(celerySignalProcessor, self).handle_save(sender,instance,  **kwargs)

@app.task()
def reindex_mymodel(sender, instance):
    ProjectIndex.update_object(ProjectIndex(), instance)




