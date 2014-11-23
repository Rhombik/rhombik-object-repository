# -*- coding: utf-8 -*-

# Scrapy settings for spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
BOT_NAME = 'spider'

SPIDER_MODULES = ['scraper.spider.spiders']
NEWSPIDER_MODULE = 'scraper.spider.spiders'
LOG_LEVEL = 'DEBUG'

ITEM_PIPELINES = {
    'scraper.spider.pipelines.saveProject': 500,
    'scraper.spider.pipelines.saveThing': 550
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'rhombik-object-repository public spider #please configure with your own name.'
