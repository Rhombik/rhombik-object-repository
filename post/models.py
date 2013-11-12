from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime
import thumbnailer.shadowbox
from django.conf import settings
from taggit.managers import TaggableManager
from filemanager.models import fileobject



	

class Post(models.Model):

    def select_thumbnail(post):
    
        print(post)
       #post=Post.objects.filter(title=title)
        files=fileobject.objects.filter(post=post)###  This gets a list of files from the post
        noThumb = True
        for fl in files:
            if fl.filetype != 'norender' and fl.filename != post.thumbnail:### Look for thumbnailable pic.
                noThumb = False
                post.thumbnail = fl
                post.save()
                print("I set " + str(post) + "'s thumbnail to " + str(fl)) 
               #self.thumbnail = fl
               #break
        if noThumb:
            post.thumbnail = fileobject.objects.all()[0] ## !!!!! THIS SETS THE THUMBNAIL. It sets it to whatever the first uploaded image is. This should be something better asap.
            post.save()


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

   #def __init__(self):
   #    self.thumbnail.limit_choices_to({'post' = self })

    def __unicode__(self):
        return self.title
    def save(self):

        #Generates the thumbnail
        ##make certain the selected thumbnail is valid, and generate

#        if self.thumbnail:
#            try:
                #I hate names.
#                thumbnail = thumbnailer.thumbnailer.thumbnail(settings.MEDIA_ROOT+"uploads/" + str(self.pk) + self.thumbnail,(128,128))
#                thumbnail[2] != "norender"
#                self.thumbnailpath = thumbnail[0]
#            except:
#                def clean(self):
#                    from django.core.exceptions import ValidationError
#                    raise ValidationError('No valid thumbnail')
#        else:
            #If no thumbnail is selected, pick one randomly and generate a thumb
#            postfiles = filemanager.models.fileobject.objects.filter(post=self).exclude(filetype="norender")[0]
#            self.thumbnailpath = thumbnailer.thumbnailer.thumbnail(postfiles.filename.path,(128,128))[0]
        import markdown
        #Markdownifies the post body, striping out any raw html
        if self.allow_html == False and self.body:
            renderedtext = markdown.markdown(self.body, safe_mode=True)
            self.body_rendered = thumbnailer.shadowbox.run(renderedtext, str(self.pk))
            super(Post, self).save() # Call the "real" save() method.
        #mardownifies the body of the post, leaving any raw HTML intact.
        elif self.body:
            renderedtext = markdown.markdown(self.body)
            self.body_rendered = thumbnailer.shadowbox.run(renderedtext, str(self.pk))
            super(Post, self).save() # Call the "real" save() method.
        else:
            super(Post, self).save()
