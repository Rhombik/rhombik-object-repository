from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import thumbnailer.thumbnailer
import os
from django.conf import settings


# Create your models here.

class userProfile(models.Model):

    user = models.ForeignKey(User, unique=True)

    ###this to be replaced when I figure out how to grab date created from user
    created = models.DateTimeField(auto_now_add = True)

    #username = models.CharField(max_length=30, blank=True, null=True)
    profilePic = models.CharField(max_length=64, default="/")
    profilePicPath = models.CharField(max_length=256, blank=True, null=True)
    bio = models.CharField(max_length=256, blank=True,  default="I didn't really care to tell you about myself, so the developers wrote this.")
    

#    def __unicode__(self):
    
    def save(self, force_insert=False, force_update=False, using=None):##def save(self):
        #created the folder for that post if it doesn't exist
        directory = settings.MEDIA_ROOT+"userPics/" ##+ self.profilePic
        if not os.path.exists(directory):
            os.makedirs(directory)
        #Generates the thumbnail
        try:
                #I hate names.
            print(str(settings.MEDIA_ROOT + "userPics" + self.profilePic))
            self.profilePicPath = thumbnailer.thumbnailer.thumbnail(str(settings.MEDIA_ROOT + "userPics" + self.profilePic), (250,250))[0]
        except:
           def clean(self):
                from django.core.exceptions import ValidationError
                raise ValidationError('No valid thumbnail')


        super(userProfile, self).save()

User.profile = property(lambda u: userProfile.objects.get_or_create(user=u)[0])
