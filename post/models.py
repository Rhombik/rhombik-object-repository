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

    rating = RatingField(can_change_vote=True)

    def __unicode__(self):
        return self.title
    def save(self):

        import markdown
        if self.allow_html == False and self.body:
            renderedtext = markdown.markdown(self.body, safe_mode=True)
            self.body_rendered = thumbnailer.shadowbox.run(renderedtext, str(self.pk))
            super(Post, self).save() # Call the "real" save() method.
        elif self.body:
            renderedtext = markdown.markdown(self.body)
            self.body_rendered = thumbnailer.shadowbox.run(renderedtext, str(self.pk))
            super(Post, self).save() # Call the "real" save() method.
        else:
            super(Post, self).save()
