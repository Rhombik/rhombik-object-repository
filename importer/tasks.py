
import os
import re
from django.contrib.auth.models import User
from project.models import Project
from filemanager.models import fileobject
from django.conf import settings
import urllib2
import lxml
from lxml.html import html5parser
from lxml import html
from lxml import etree
import urlparse

from jobtastic import JobtasticTask

def get_response(url):

    import urllib2,cookielib

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                  'Accept-Encoding': 'none',
                  'Accept-Language': 'en-US,en;q=0.8',
                  'Connection': 'keep-alive'}
    
    req = urllib2.Request(url, headers=hdr)
    
    #try:
    response = urllib2.urlopen(req)
    #except urllib2.HTTPError, e:
    #    pass#print(e.fp.read())
    return(response)

from Settings.celery import app
from celery import Celery,shared_task,chord,signature

class ThingiUserTask(JobtasticTask):
    """
    The user want's all of thier things.
    """
    significant_kwargs = [
                ('url', str),
                ('userPK', str),
           ]
    herd_avoidance_timeout = 180
    def calculate_result(self, url="", userPK=None, **kwargs):
        response=get_response(url)
        dom=html.fromstring(response.read())
        designLinkattempt = dom.xpath('//a[contains(@href,"designs")]/@href')[0]
        print("designLinkTail : {}".format(designLinkattempt))
        designsLink=urlparse.urljoin('http://www.thingiverse.com/',designLinkattempt)
        print("designslink : {}".format(designsLink))
        response=get_response(designsLink)
        dom=html.fromstring(response.read())
        paginationUrlTails=dom.xpath('//*[contains(@class,\'pagination\')]/ul/li/a/@href')
        print(paginationUrlTails)
        paginationNumbers = [int(re.search('page:(\d+?)\?', paginationUrl).group(1)) for paginationUrl in paginationUrlTails]
        print("paginationNumbers : {}".format(paginationNumbers))
        paginationTail = "/page:{0}?sort=recent&filter=&search="
        paginationUrls = [designsLink+paginationTail.format(pgNum) for pgNum in range(1,sorted(paginationNumbers)[-1]+1)]
        print("paginationUrls : {}".format(paginationUrls))
        for paginationUrl in paginationUrls:
            print("Calling GetThingiProjectTask on {}".format(paginationUrl))
            GetThingiProjectTask.delay(url=paginationUrl,userPK=userPK)
class GetThingiProjectTask(JobtasticTask):
    significant_kwargs = [
                ('url', str),
                ('userPK', str),
           ]
    herd_avoidance_timeout = 180
    def calculate_result(self, url="", userPK=None, **kwargs):
        print("reading thing links from {}".format(url))
        response=get_response(url)
        dom=html.fromstring(response.read())
        things=dom.xpath('//a[contains(@href,\'thing:\')]/@href')
        things=['http://www.thingiverse.com/'+t for t in things if ('#comments' not in t) and ('edit' not in t)]
        print("things : {}".format(things))
        for projecturl in things:
            print("Calling ThingiProjectTask on {}".format(projecturl))
            ThingiProjectTask.delay(url=projecturl,userPK=userPK)

class ThingiProjectTask(JobtasticTask):
    """
    Things are there, but users want them here. Lets go get them!
    In due time.
    """
    significant_kwargs = [
                ('url', str),
                ('userPK', str),
           ]
    herd_avoidance_timeout = 180
    def calculate_result(self, url, userPK, **kwargs):
        print("importing project : {}".format(url))
        response=get_response(url)
        goo=response.read()
        dom=html.fromstring(goo)
        #print(dom.xpath('//*[contains(@class,\'thing-header-data\')]/h1/text()'))
        
        # Getting some metadatas for the project.
        #this is probably fine. If you're confused, feel free to make it more verbose.
        project=Project()
        project.author_id = userPK# User.objects.get(pk=userPK)
        project.title = dom.xpath('//*[contains(@class,\'thing-header-data\')]/h1/text()')[0].strip()
        tags = dom.xpath("//*[contains(@class,\'thing-info-content thing-detail-tags-container\')]/div/a/text()")
        
        project.draft=True
        
        if Project.objects.filter(title=project.title):
            import datetime
            project.title+= " -- "+str(datetime.datetime.today())
        
        project.save()
        for tag in tags:
           project.tags.add(tag)

        ## get special text files. (readme, instructions, license)
        import html2text
        h2t = html2text.HTML2Text()
        #Get the reame file, do stuff to it.
        readme = etree.tostring(dom.xpath("//*[@id = 'description']")[0])
        readme = readme.encode("utf-8")
        readme = h2t.handle(readme)
        import unicodedata
        readmeItem=fileobject()
        readmeItem.parent=project#projectObject['SID']
        readmeItem.isReadme = True
        readmename="README.md"
        readmefile=u""+unicodedata.normalize('NFKD',readme).encode('ascii','ignore')
        print(readmename)
        print(readmefile)
        readmeItem.fromText(readmefile,readmename)
        readmeItem.save()
        project.bodyFile=readmeItem
        project.save()
        print("bodyFile:")
        print(project.bodyFile)
        #projectObject['readme'] = u""+unicodedata.normalize('NFKD',readme).encode('ascii','ignore')
        #also a markdown file I guess we'd want.
        try:
            instructions = etree.tostring(dom.xpath("//*[@id = 'instructions']")[0])
            instructions = u""+h2t.handle(instructions).encode('ascii','ignore')
            instructionItem=fileobject()
            instructionItem.parent=project#Object['SID']
            name="Instructions.md"
            filename=instructions
            instructionItem.fromText(filename,name)
            instructionItem.save()
        except IndexError:
            pass
            #print("xpath to get the instructions IndexError'd")

        ## now, because the format of the license on thingi is always the same, we can pull this off.
        ## but I expect it is rather fragile.
        licenseurl =dom.xpath("//*[contains(@class,\'license-text\')]/a/@href")[2].strip()
        licensetext = dom.xpath("//*[contains(@class,\'license-text\')]/a/text()")[1].strip()
        licenceItem=fileobject()
        licenceItem.parent=project#Object['SID']
        lname="License.md"
        lfile="["+licensetext+"]("+licenseurl+")"
        licenceItem.fromText(lfile,lname)
        licenceItem.save()

        ## get all the projects image and file objects
        #grab files
        filelist = dom.xpath('//*[contains(@class,\'thing-file\')]/a/@href')
        #Grab only raw images.        
        imagelist = dom.xpath('//*[contains(@class,\'thing-gallery-thumbs\')]/div[@data-track-action="viewThumb"][@data-thingiview-url=""]/@data-large-url')
        fileurls=[urlparse.urljoin('http://www.thingiverse.com/', fl) for fl in imagelist+filelist]
        print("fileurls:")
        print(fileurls)
        bundle_o_tasks=[ThingiFileTask().si(url=i,projectPK=project.pk) for i in fileurls]
        filetask = chord(bundle_o_tasks)(ResaveProjectTask().si(projectPK=project.pk))
        return(project.title)


class ThingiFileTask(JobtasticTask):
    '''Get an individual file... AND SAVE IT! AH HA HA HA!!!'''
    significant_kwargs = [
                ('url', str),
                ('projectPK', str),
           ]
    herd_avoidance_timeout = 120
    ignore_result=True
    def calculate_result(self, url, projectPK, **kwargs):
        print("downloading {}".format(url))
        response=get_response(url)

        name=urlparse.urlparse(response.url)[2].split("/")[-1]
        name=name.replace("_display_large","")
        print(name)

        fileobjectInstance=fileobject()
        fileobjectInstance.parent=Project.objects.get(pk=projectPK)

        from django.core.files.base import ContentFile
        fileobjectInstance.filename = ContentFile('')
        fileobjectInstance.filename.name = name
        while True:
            chunk = response.read(2048)
            if not chunk:
                break
            fileobjectInstance.filename.write(chunk)
        print('done')
        
        #fileobjectInstance.filename = newFile#.save(name,newFile)
        fileobjectInstance.filename.close()

        super(fileobject,fileobjectInstance).save()
        return(url,projectPK)

class ResaveProjectTask(JobtasticTask):
    '''goo'''
    significant_kwargs = [
                ('projectPK', str),
           ]
    herd_avoidance_timeout = 120
    ignore_result=True

    def calculate_result(self,projectPK, **kwargs):
        print("saveing project again")
        project=Project.objects.get(pk=projectPK)
        project.save(enf_valid=True)
        return("{} resaved".format(project))
