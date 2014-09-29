# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scraper.spider.items import ProjectItem, fileObjectItem
from scrapy.contrib.linkextractors import LinkExtractor
import re
import urlparse

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log, signals

def runScraper(urls):
    spider = ThingiverseSpider(start_urls=urls)
    crawler = Crawler(Settings())
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start()
    reactor.run()

class ThingiverseSpider(CrawlSpider):
    name = "thingiverse"
    allowed_domains = ["thingiverse.com"]
    ##Find the links.
    print(start_urls)
    def parse(self, response):
        print(response)
        design = LinkExtractor(allow=('design')).extract_links(response)
        if design:
            yield scrapy.http.Request(url=design[0].url, callback=self.projectGet)
        if re.search('thing:\d\d+',response.url):
            yield scrapy.http.Request(url=response.url, callback=self.project)

    def projectGet(self, response):
        ##Get next pages. We can be really lazy due to the scrapy dedupe
        paginatorlinks=response.selector.xpath('//*[contains(@class,\'pagination\')]/ul/li/a/@href').extract()
        #:/ I guess this makes sense.
        paginatorlinks.pop(0)
        for i in paginatorlinks:
            yield scrapy.http.Request(url=urlparse.urljoin(response.url, i), callback=self.projectGet)

        objects = LinkExtractor(allow=('thing:\d\d+')).extract_links(response)
        for i in objects:
            yield scrapy.http.Request(url=i.url, callback=self.project)

    def project(self,response):
        projectObject=ProjectItem()
        projectObject['title']=response.selector.xpath('//*[contains(@class,\'thing-header-data\')]/h1/text()').extract()[0].strip()
        projectObject['readme']=response.selector.xpath("//*[@id = 'description']/text()").extract()[0].strip()
        yield projectObject
        #Grab only raw images.        
        imagelist = response.selector.xpath('//*[contains(@class,\'thing-gallery-thumbs\')]/div[@data-track-action="viewThumb"][@data-thingiview-url=""]/@data-large-url')
        filelist = response.selector.xpath('//*[contains(@class,\'thing-file\')]/a/@href')
        for i in filelist:
            pass
        #    yield scrapy.http.Request(url=urlparse.urljoin(response.url, i.extract()), callback=self.item, meta={'parent':projectObject['SID']})
        for i in imagelist:
            pass
          #  yield scrapy.http.Request(url=urlparse.urljoin(response.url, i.extract()), callback=self.item, meta={'parent':projectObject['SID']})


    def item(self,response):
        item=fileObjectItem()
        item['parent'] = response.meta['parent']
        item['filename']=response.body
        yield(item)

