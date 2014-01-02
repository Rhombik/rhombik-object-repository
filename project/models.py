from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime
import thumbnailer.shadowbox
from django.conf import settings
from taggit.managers import TaggableManager
from filemanager.models import fileobject
from updown.fields import RatingField	


##Does this actuall work? I don't think it does.... It seems to always return(SET_NULL)
##I've disabled it. Now whenever a fileobject gets deleted, it starts a task checking for null fields.
def select_thumbnail(instance):
   #project=Project.objects.filter(title=title)
    files=fileobject.objects.filter(pk=instance)###  This gets a list of files from the project
    for fl in files:
        if fl.filetype != 'norender' and fl.filetype != "text" and fl.filename != project.thumbnail:### Look for thumbnailable pic.
            project.thumbnail = fl
            return (fl)
    if noThumb:
        #project.thumbnail = fileobject.objects.all()[0] ## !!!!! THIS SETS THE THUMBNAIL. It sets it to whatever the first uploaded image is. This should be something better asap.
        return(SET_NULL)


class Project(models.Model):

    title = models.CharField(max_length=60,blank=True, null=True, unique=True)
    thumbnail = models.ForeignKey('filemanager.fileobject', blank=True, null=True, on_delete=models.SET_NULL , related_name='thumbnail')
    body = models.TextField(blank=True, null=True)

    #This exists soley so that we can find prohects that don't have a readme.
    bodyFile = models.ForeignKey('filemanager.fileobject', blank=True, null=True, on_delete=models.SET_NULL , related_name='readme')

    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    author = models.ForeignKey(User, related_name='author',default=User)
    allow_html = models.BooleanField(default=False)
    ##only used internally, don't set
   #body_rendered = models.TextField('Entry body as HTML', blank=True, null=True)
    tags = TaggableManager(blank=True)
    draft = models.BooleanField(default=False)

    rating = RatingField(can_change_vote=True)

    def __unicode__(self):
        return self.title
    def save(self):
        if not self.thumbnail:
            print(self.thumbnail)
            self.draft=True
        super(Project, self).save()

