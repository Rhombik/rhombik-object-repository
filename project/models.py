from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime
import thumbnailer.shadowbox
from django.conf import settings
from taggit.managers import TaggableManager
from filemanager.models import fileobject, fileuploadpath
from djangoratings.fields import RatingField
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
import project.tasks

class Project(models.Model):

    title = models.CharField(max_length=60,blank=True, null=True, unique=True)
    thumbnail = models.ForeignKey('filemanager.fileobject', blank=True, null=True, on_delete=models.SET_NULL, related_name='thumbnail',)
    body = models.TextField(blank=True, default="")

    #This exists soley so that we can find projects that don't have a readme.
    bodyFile = models.ForeignKey('filemanager.fileobject', blank=True, null=True, related_name='readme', on_delete=models.SET_NULL)

    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    author = models.ForeignKey(User, related_name='author',)
    allow_html = models.BooleanField(default=False)
    ##only used internally, don't set
    tags = TaggableManager(blank=True)
    draft = models.BooleanField(default=False)

    ##Depricated
    valid = True

    downloadcount = RatingField(range=1,allow_delete = False,allow_anonymous = True,) 

    rating = RatingField(range=2, can_change_vote = True,allow_delete = True,)
    ratingSortBest = models.FloatField(default=1)
    ratingCount = models.IntegerField(blank=True, null=True)
    class Meta:
        permissions = (
            ('view', 'View'),
            ('edit', 'Edit'),
        )

    def updateReadme(self, text):
        if self.bodyFile:
            print(text)
            self.bodyFile.fromText(text)
        else:
            newFileObject = fileobject.objects.create(parent=self)
            newFileObject.fromText(text, title="README.md")
            newFileObject.save()
            newFileObject.filename.close()

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
            readme = self.bodyFile.filename.read()
        except AttributeError as e:
            if str(e) == "'NoneType' object has no attribute 'filename'":
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
                thumbnailstring = ""

        return ProjectForm({'title':self.title, 'body': readme, 'thumbnail': thumbnailstring, 'tags' : tags}, self)

    def checkValidity(self):
        return(self.get_form().is_valid())

    def enf_validity(self):
        print("enf_validity is depricated, asshole.")
        pass

    def enf_consistancy(self):
        #checks if there's a thumbnail.
        if not self.thumbnail:
            object_type = ContentType.objects.get_for_model(self)
            files = fileobject.objects.filter(content_type=object_type,object_id=self.id).exclude(filetype='norender').exclude(filetype='text')
            if files:
                self.thumbnail = files[0]
                super(Project, self).save()
                return True
            else:
                if not self.draft:
                    self.draft = True
                    super(Project, self).save()
                return False
        elif self.thumbnail:
            return True

    def __unicode__(self):
        if self.title:
             return self.title
        else:
             return "Untitled Project"
