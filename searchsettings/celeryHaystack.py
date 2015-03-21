from django.db import models
from haystack import signals
from celery import Celery, shared_task
import os
from project.search_indexes import ProjectIndex
from haystack.query import SearchQuerySet
from project.models import Project

app = Celery('tasks')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Settings.settings')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


class celerySignalProcessor(signals.RealtimeSignalProcessor):
    def setup(self):
        # Listen only to the ``User`` model.
        models.signals.post_save.connect(self.handle_save, sender=Project)
        models.signals.post_delete.connect(self.handle_delete, sender=Project)
    def teardown(self):
        # Disconnect only for the ``User`` model.
        models.signals.post_save.disconnect(self.handle_save, sender=Project)
        models.signals.post_delete.disconnect(self.handle_delete, sender=Project)

    def handle_save(self, sender, instance, **kwargs):
        if type(instance) == Project and instance.draft==False:
            reindex_mymodel.delay(sender, instance)
        if type(instance) == Project and instance.draft==True:
            delete_mymodel.delay(sender, instance)
    def handle_delete(self, sender, instance, **kwargs):
        delete_mymodel.delay(sender, instance)


@app.task()
def reindex_mymodel(sender, instance):
    ProjectIndex.update_object(ProjectIndex(), instance)

@app.task()
def delete_mymodel(sender, instance):
    ProjectIndex.remove_object(ProjectIndex(), instance)

