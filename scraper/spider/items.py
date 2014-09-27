# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.djangoitem import DjangoItem
from project.models import *
from scraper.spider.djangoAutoItem import CountedItem

class ProjectItem(CountedItem):
    django_model = Project
    readme = scrapy.Field()

class fileObjectItem(DjangoItem):
    django_model = fileobject
    parent = scrapy.Field()

