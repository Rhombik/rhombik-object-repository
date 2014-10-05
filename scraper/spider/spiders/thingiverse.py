# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scraper.spider.items import ProjectItem, fileObjectItem
from scrapy.contrib.linkextractors import LinkExtractor
import re
import urlparse

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from scraper.spider.settings import ITEM_PIPELINES

def runScraper(urls):
    spider = ThingiverseSpider(urls)
    settings = get_project_settings()
    settings.set('LOG_ENABLED', False)
    settings.set('ITEM_PIPELINES', ITEM_PIPELINES)
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    reactor.run()

class ThingiverseSpider(CrawlSpider):
    name = "thingiverse"
    allowed_domains = ["thingiverse.com"]
    ##Find the links.
    start_urls = None
    def __init__(self, start_urls, *args, **kwargs):
        self.start_urls = start_urls
        super(ThingiverseSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        requests=[]
        for i in self.start_urls:
            requests.append(scrapy.http.Request(url=i, callback=self.parse, dont_filter=True))
        return requests

    def parse(self, response):
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
        	yield scrapy.http.Request(url=urlparse.urljoin(response.url, i.extract()), callback=self.item, meta={'parent':projectObject['SID']})
        for i in imagelist:
	    print("IMAGE:::")
	    print(urlparse.urljoin(response.url, i.extract()))
            yield scrapy.http.Request(dont_filter=True, url=urlparse.urljoin(response.url, i.extract()), callback=self.item, meta={'parent':projectObject['SID']})


    def item(self,response):
        item=fileObjectItem()

        ## warning stupid preasent here.
	# splitting and grabing from urlparse for filename may not be best.
        item['name']=urlparse.urlparse(response.url)[2].split("/")[-1]
	item['name']=item['name'].replace("_display_large","")

        item['parent'] = response.meta['parent']
        item['filename']=response.body
        yield(item)
