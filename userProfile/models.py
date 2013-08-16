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
    profilePic = models.CharField(max_length=64)
    profilePicPath = models.CharField(max_length=256, blank=True, null=True)
    bio = models.CharField(max_length=256)
    

#    def __unicode__(self):
    
    def save(self):
        #created the folder for that post if it doesn't exist
        directory = settings.MEDIA_ROOT+"userPics/" ##+ self.profilePic
        if not os.path.exists(directory):
            os.makedirs(directory)
        #Generates the thumbnail
        try:
                #I hate names.
            print(str(settings.MEDIA_ROOT + "userPics" + self.profilePic))
            self.profilePicPath = thumbnailer.thumbnailer.thumbnail(str(settings.MEDIA_ROOT + "userPics" + self.profilePic), (200,200))[0]
        except:
            print("thumbnail failed")

        super(userProfile, self).save()
