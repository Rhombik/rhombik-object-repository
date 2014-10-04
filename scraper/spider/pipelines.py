# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scraper.spider.items import *
import project.models as project
import filemanager.models as files
import djangoAutoItem
from django.contrib.auth.models import User

class saveProject(object):
    def process_item(self, item, spider):
        if type(item) == type(ProjectItem()):
            if not hasattr(item, 'author'):
                item['author']= User.objects.filter(pk=1)[0]
            item.save()
        return item

class saveThing(object):
    def process_item(self, item, spider):
        if type(item) == type(fileObjectItem()):
           item['parent']=djangoAutoItem.SIDmap[item['parent']]
           item.save()
        return item

class saveProjectAgain(object):
    def process_item(self, item, spider):
        if type(item) == type(ProjectItem()):
            newitem = djangoAutoItem.SIDmap[item['SID']]
            newitem.save()
        return item

