# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from spider.items import *
import project.models as project
import filemanager.models as files
import djangoAutoItem

class saveProject(object):
    def processs_item(self, item, spider):
        print("save project")
        if type(item) == type(ProjectItem()):
            item.save()
            print(str(djangoAutoItem.SIDmap)+"----sidmap")
        return item

class saveThing(object):
    def process_item(self, item, spider):
        if type(item) == type(fileObjectItem()):
           pass
#           item.save()
        return item
