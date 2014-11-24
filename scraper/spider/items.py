# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.djangoitem import DjangoItem
from project.models import *
from filemanager.models import *
from scraper.spider.djangoAutoItem import CountedItem
from django.contrib.auth.models import User

class ProjectItem(CountedItem):
    django_model = Project


class fileObjectItem(DjangoItem):
    django_model = fileobject
    name = scrapy.Field()
    parent = scrapy.Field()
    isReadme = scrapy.Field()
    def save(self):
        fobj=fileobject()
	project=Project.objects.get(pk=self['parent']['pk'])
        fobj.parent=project

        fobj.fromText(self['name'],self['filename'])

	fobj.save()

	if 'isReadme' in self:
	    if self['isReadme']:
	        project.bodyFile=fobj
	        project.save()


