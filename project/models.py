from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime
import thumbnailer.shadowbox
from django.conf import settings
from taggit.managers import TaggableManager
from filemanager.models import fileobject
from djangoratings.fields import RatingField
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
import project.tasks
##Does this actuall work? I don't think it does.... It seems to always return(SET_NULL)
##I've disabled it. Now whenever a fileobject gets deleted, it starts a task checking for null fields.
def select_thumbnail(instance):
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
   #thumbnail = models.ForeignKey('filemanager.fileobject', blank=True, null=True, on_delete=models.SET_NULL , related_name='thumbnail')
    thumbnail = models.ForeignKey('filemanager.fileobject', blank=True, null=True, on_delete=models.SET_DEFAULT, related_name='thumbnail', default=None)
    body = models.TextField(blank=True, null=True)

    #This exists soley so that we can find projects that don't have a readme.
    bodyFile = models.ForeignKey('filemanager.fileobject', blank=True, null=True, related_name='readme', on_delete=models.SET_NULL)

    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    author = models.ForeignKey(User, related_name='author',default=User)
    allow_html = models.BooleanField(default=False)
    ##only used internally, don't set
   #body_rendered = models.TextField('Entry body as HTML', blank=True, null=True)
    tags = TaggableManager(blank=True)
    draft = models.BooleanField(default=False)
    valid = models.BooleanField(default=False)

    downloadcount = RatingField(range=1,allow_delete = False,allow_anonymous = True,) 


    rating = RatingField(range=2, can_change_vote = True,allow_delete = True,)
    ratingSortBest = models.FloatField(default=1)
    ratingCount = models.IntegerField(blank=True, null=True)
    #Pretends that 0 is -1 and 1 is 1.
    def calc_adjusted_rating(self):
        import math
        #The total score (you can vote 1 or 2) of all the votes, minus the number of people who have voted.
        upvotes = self.rating.score - self.rating.votes
        #Total number of people who voted minus upvotes
        downvotes = self.rating.votes - upvotes
        self.ratingCount = upvotes-downvotes
        votes = self.rating.votes


        #http://www.evanmiller.org/how-not-to-sort-by-average-rating.html
        if(votes == 0):
            #Set to 2 by default, to encourage people to look at/vote on new content. 
            self.ratingSortBest = 1 
        else: 
            r=1.0*upvotes/votes
            z=1.95 
            self.ratingSortBest = ((r+z*z-z*math.sqrt((r*(1-r)+(z*z/4*votes))/votes))/(1+z*z/votes))

        super(Project, self).save()

    def save(self, enf_valid=False):
        super(Project, self).save()
        self.enf_consistancy()

        if enf_valid:
            self.enf_validity()

    def delete(self):
        project.tasks.fileEnforcer.delay(self)
        super(Project, self).delete()

    def get_form(self):
        from os import path
        from project.forms import ProjectForm
        if self.title:
            title = self.title
        else:
            title = ""

        try:
            print("1")
            readme = self.bodyFile.filename.read()
            print("2")
        except AttributeError as e:
            if str(e) == "'NoneType' object has no attribute 'filename'":
                print("The filename does not yet exist. It's fine.")
                readme = ""
            else:
                raise

        taglist = []
        for i in self.tags.names():
           taglist.append(i)
        tags = ",".join(taglist)

        try:
            thumbnailstring = "/"+path.split(self.thumbnail.filename.url)[1]
        except AttributeError as e:
            if str(e) == "'NoneType' object has no attribute 'filename'":
                print("There was no thumbnail. This is to be expected sometimes.")
                thumbnailstring = ""

        return ProjectForm({'title':self.title, 'body': readme, 'thumbnail': thumbnailstring, 'tags' : tags}, self)

    def enf_validity(self):
        form = self.get_form()
        print("CHECKING IF VALID")
        if form.is_valid():
            print("IS VALID")
            self.valid=True
            super(Project, self).save()
        else:
            print(form.errors)

    def enf_consistancy(self):
        #checks if there's a thumbnail.

        #Sometimes the "thumbnail = models.ForeignKey" key doesn't get set to null fast enough. This checks to see if the key points to a thumbobject that doesn't actually exist, or if the key is null.
        try:
            if self.thumbnail:
                getnewthumb=False
            else:
                getnewthumb=True
        except:
            getnewthumb=True

        if getnewthumb:
            object_type = ContentType.objects.get_for_model(self)
            files = fileobject.objects.filter(content_type=object_type,object_id=self.id)
            for fl in files:
                if fl.filetype != 'norender' and fl.filetype != "text":### Look for thumbnailable pic.
                    self.thumbnail = fl
                    super(Project, self).save()
                    return True
            self.draft = True
            super(Project, self).save()
            return False
        else:
            return True

    def __unicode__(self):
        if self.title:
             return self.title
        else:
             return "Untitled Project (A Draft..?)"

