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

from django.contrib.auth.models import User

def runScraper(urls, user):
    userID=user.pk
    spider = ThingiverseSpider(urls, user=user)
    settings = get_project_settings()
    settings.set('LOG_ENABLED', False)
    settings.set('ITEM_PIPELINES', ITEM_PIPELINES)
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    reactor.run(installSignalHandlers=0)

class ThingiverseSpider(CrawlSpider):
    name = "thingiverse"
    allowed_domains = ["thingiverse.com"]
    ##Find the links.
    start_urls = None
    def __init__(self, start_urls, user=None, *args, **kwargs):
        self.start_urls = start_urls
	if not user:
            user = User.objects.filter(pk=1)[0]
	self.user_id=user.pk
        super(ThingiverseSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        requests=[]
        for i in self.start_urls:
            requests.append(scrapy.http.Request(url=i, callback=self.parse, dont_filter=True))
        return requests

    def parse(self, response):
        ## if it's a thing it's not a project.
        if re.search('thing:\d\d+',response.url):
            print("SCRAPING THING : "+response.url)
            yield scrapy.http.Request(url=response.url, callback=self.project)
        else:
            ## sometimes thing pages link to other things with the 'design' tag. I haven't seen this on a user page.
            design = LinkExtractor(allow=('design')).extract_links(response)
            if design:  
                print("GOING TO "+design[0].url+" TO SCRAPE SOME STUFF!!!")
                yield scrapy.http.Request(url=design[0].url, callback=self.projectGet)

    def projectGet(self, response):
        ##Get next pages. We can be really lazy due to the scrapy dedupe
        paginatorlinks=response.selector.xpath('//*[contains(@class,\'pagination\')]/ul/li/a/@href').extract()
        #:/ I guess this makes sense.
        from exceptions import IndexError
        try:
            paginatorlinks.pop(0)
        except IndexError as e:
            # e.message is dep, I guess using str(e) returning the message now is the thing.
            if str(e) == "pop from empty list":
                print("paginator returned empty. S'all good though.")
            else:
                raise
        for i in paginatorlinks:
            yield scrapy.http.Request(url=urlparse.urljoin(response.url, i), callback=self.projectGet)

        objects = LinkExtractor(allow=('thing:\d\d+')).extract_links(response)
        for i in objects:
            # Teh hax! scrapy's dupefilter sees "foo.bar" and "foo.bar/" as different sites. This is bad. Maybe this should be pushed to scrapy proper...
            if i.url[-1] == '/':
                i.url=i.url[:-1]
            yield scrapy.http.Request(url=i.url, callback=self.project)

    def project(self,response):
        projectObject=ProjectItem()
        projectObject['author']=User.objects.get(pk=self.user_id)
        projectObject['title']=response.selector.xpath('//*[contains(@class,\'thing-header-data\')]/h1/text()').extract()[0].strip()

        import html2text
        h2t = html2text.HTML2Text()
        h2t.ignore_links = True
        #Get the reame file, do stuff to it.
        readme =  h2t.handle(response.selector.xpath("//*[@id = 'description']").extract()[0].strip())
        projectObject['readme'] = readme
        print("PROJECT OBJECT "+projectObject['title']+" getting yielded")
        #also a markdown file I guess we'd want.
        try:
            instructions =  h2t.handle(response.selector.xpath("//*[@id = 'instructions']").extract()[0].strip())
        except IndexError:
            print("xpath to get the instructions IndexError'd")
        licenseurl =response.selector.xpath("//*[contains(@class,\'license-text\')]/a/@href")[2].extract()
	projectObject['license']=h2t.handle(licenseurl)
        tags = response.selector.xpath("//*[contains(@class,\'thing-info-content thing-detail-tags-container\')]/a/text()").extract()
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

    def closed(self, *args, **kwargs):
        print("HI I EXIST, I AM THE CLOSE METHOD!!!")
        from scraper.spider import djangoAutoItem
        from project.models import Project
        from exceptions import KeyError
        for key in djangoAutoItem.SIDmap:
            try:
                project=Project.objects.get(title=djangoAutoItem.SIDmap[key]['title'])
                print("saving "+str(project)+" again.")
                project.save(enf_valid=True)
            except KeyError as e:
                if str(e)=="'title'":
                    print("This SIDmap thing has no title. therefore we are not going to save it again.")
                else:
                    raise


    def item(self,response):
        item=fileObjectItem()

        ## warning stupid preasent here.
	# splitting and grabing from urlparse for filename may not be best.
        item['name']=urlparse.urlparse(response.url)[2].split("/")[-1]
	item['name']=item['name'].replace("_display_large","")

        item['parent'] = response.meta['parent']
        item['filename']=response.body
        yield(item)

