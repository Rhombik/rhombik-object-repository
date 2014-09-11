##Like the sandard djangoItem, but with an auto-incrementing "sid" field, and code to map sid's to pk's once the item has been saved.
import itertools
import scrapy
import scrapy.contrib.djangoitem

SIDcount = itertools.count()
SIDmap = {}

class CountedItem(djangoitem.DjangoItem):
    def __init__(self):
        super(CountedItem, self).__init__()
        self['SID'] = next(SIDcount)
        SID[self['SID']] = {}
    #scrapy ID
    SID = scrapy.fields()
    def save(self):
        super(countedItem, self).save()
        SID[self['SID']]['django_model']=self.django_model
        SID[self['SID']]['pk']=self.pk
