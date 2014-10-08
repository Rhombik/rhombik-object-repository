# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scraper.spider.items import *
import project.models as project
import filemanager.models as files
import djangoAutoItem
import datetime
from project.models import Project
class saveProject(object):
    def process_item(self, item, spider):
        if type(item) == type(ProjectItem()):
	    print("user is ::::::::::::::::")
	    print(item['author'])
            item['draft']=True
            if not Project.objects.filter(title=item['title']):
                item.save()
            else:
                item['title']+= " -- "+str(datetime.datetime.today())
                item.save()
        return item

class saveThing(object):
    def process_item(self, item, spider):
        if type(item) == type(fileObjectItem()):
           print("THE SIDmap:::")
           print(djangoAutoItem.SIDmap)
           item['parent']=djangoAutoItem.SIDmap[item['parent']]
           item.save()
        return item

class saveProjectAgain(object):
    def process_item(self, item, spider):
        if type(item) == type(ProjectItem()):
            newitem = djangoAutoItem.SIDmap[item['SID']]
            newitem.save()
        return item

