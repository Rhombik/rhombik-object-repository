from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime
import thumbnailer.shadowbox
from django.conf import settings
from taggit.managers import TaggableManager
from filemanager.models import fileobject
from updown.fields import RatingField	

class Project(models.Model):

    def select_thumbnail(project):
    
       #project=Project.objects.filter(title=title)
        files=fileobject.objects.filter(project=project)###  This gets a list of files from the project
        noThumb = True
        for fl in files:
            if fl.filetype != 'norender' and fl.filetype != "text" and fl.filename != project.thumbnail:### Look for thumbnailable pic.
                noThumb = False
                project.thumbnail = fl
                project.save()
                print("project.models set " + str(project.name) + "'s thumbnail to " + str(fl)) 
               #self.thumbnail = fl
               #break
        if noThumb:
            project.thumbnail = fileobject.objects.all()[0] ## !!!!! THIS SETS THE THUMBNAIL. It sets it to whatever the first uploaded image is. This should be something better asap.
            project.save()


    title = models.CharField(max_length=60,blank=True, null=True, unique=True)
    thumbnail = models.ForeignKey('filemanager.fileobject', blank=True, null=True, on_delete=models.SET_NULL , related_name='thumbnail')

    body = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    author = models.ForeignKey(User, related_name='author',default=User)
    allow_html = models.BooleanField(default=False)
    ##only used internally, don't set
    body_rendered = models.TextField('Entry body as HTML', blank=True, null=True)
    tags = TaggableManager(blank=True)
    draft = models.BooleanField(default=False)

    rating = RatingField(can_change_vote=True)

    def __unicode__(self):
        return self.title
    def save(self):

        import markdown
        if self.allow_html == False and self.body:
            renderedtext = markdown.markdown(self.body, safe_mode=True)
            self.body_rendered = thumbnailer.shadowbox.run(renderedtext, str(self.pk))
            super(Project, self).save() # Call the "real" save() method.
        elif self.body:
            renderedtext = markdown.markdown(self.body)
            self.body_rendered = thumbnailer.shadowbox.run(renderedtext, str(self.pk))
            super(Project, self).save() # Call the "real" save() method.
        else:
            super(Project, self).save()
