import datetime
from haystack import indexes
from celery_haystack.indexes import CelerySearchIndex
from project.models import Project


class ProjectIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author')
    created = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return Project

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.exclude(draft=True)
