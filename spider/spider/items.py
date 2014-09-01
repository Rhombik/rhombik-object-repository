# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.djangoitem import DjangoItem
from project.models import *

class ProjectItem(DjangoItem):
    django_model = Project
    files = scrapy.Field()
class fileObjectItem(DjangoItem):
    django_model = fileobject

