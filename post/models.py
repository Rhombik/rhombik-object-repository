from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime
import thumbnailer.shadowbox
import thumbnailer.thumbnailer
import os
from django.conf import settings
from taggit.managers import TaggableManager
import filemanager.models  


class Post(models.Model):

    title = models.CharField(max_length=60,unique=True)
    thumbnail = models.CharField(max_length=60, blank=True, null=True)
    thumbnailpath = models.CharField(max_length=256, blank=True, null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    author = models.ForeignKey(User, related_name='author',default=User) 
    allow_html = models.BooleanField(default=False)
    ##only used internally, don't set
    body_rendered = models.TextField('Entry body as HTML', blank=True, null=True)
    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return self.title
    def save(self):

        #Generates the thumbnail
        ##make certain the selected thumbnail is valid, and generate
        if self.thumbnail:
            try:
                #I hate names.
                thumbnail = thumbnailer.thumbnailer.thumbnail(settings.MEDIA_ROOT+"uploads/" + str(self.pk) + self.thumbnail,(128,128))
                thumbnail[2] != "norender"
                self.thumbnailpath = thumbnail[0]
            except:
                self.thumbnailpath = "invalid"
                #def clean(self):
                #    from django.core.exceptions import ValidationError
                #    raise ValidationError('No valid thumbnail')
        else:
            #If no thumbnail is selected, pick one randomly and generate a thumb
            postfiles = filemanager.models.fileobject.objects.filter(post=self).exclude(filetype="norender")[0]
            self.thumbnailpath = thumbnailer.thumbnailer.thumbnail(postfiles.filename.path,(128,128))[0]
        import markdown
        #Markdownifies the post body, striping out any raw html
        if self.allow_html == False:
            renderedtext = markdown.markdown(self.body, safe_mode=True)
            self.body_rendered = thumbnailer.shadowbox.run(renderedtext, self.title)
            super(Post, self).save() # Call the "real" save() method.
        #mardownifies the body of the post, leaving any raw HTML intact.
        else:
            self.body_rendered = markdown.markdown(self.body)
            self.body_rendered = thumbnailer.shadowbox.run(renderedtext, self.title)
            super(Post, self).save() # Call the "real" save() method.

