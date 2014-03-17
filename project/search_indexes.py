import datetime
from haystack import indexes
#from celery_haystack.indexes import CelerySearchIndex
from project.models import Project
from filemanager.models import fileobject

class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    data = indexes.NgramField()

    author = indexes.CharField(model_attr='author')
    created = indexes.DateTimeField(model_attr='created')
    tags = indexes.MultiValueField()
    def get_model(self):
        return Project

    def prepare_tags(self, obj):
        print ([tag.name for tag in obj.tags.all()])
        return [tag.name for tag in obj.tags.all()]


    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.exclude(draft=True)
