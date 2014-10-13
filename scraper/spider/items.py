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
    readme = scrapy.Field()
    def save(self):
        project=Project()
        project.valid=False
        project.author=self['author']
        project.title=self['title']
        project.save()
        project.saveReadme(self['readme'])
        project.save()
        print("this is def happening")
        super(ProjectItem, self).save()



class fileObjectItem(DjangoItem):
    django_model = fileobject
    name = scrapy.Field()
    parent = scrapy.Field()
    def save(self):
        fobj=fileobject()
        fobj.parent=Project.objects.get(title=self['parent']['title'])

        from django.core.files.uploadedfile import UploadedFile
        from io import BytesIO

        io = BytesIO(self['filename'])
        fl = UploadedFile(io)

        fobj.filename.save(self['name'], fl)

        fl.close()
        io.close()

	fobj.save()


