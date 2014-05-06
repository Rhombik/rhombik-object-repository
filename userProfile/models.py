from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import thumbnailer.thumbnailer2
import os
from django.conf import settings
from django.contrib.contenttypes import generic

# Create your models here.

class userProfile(models.Model):

    user = models.ForeignKey(User, unique=True)

    ###when the user profile was created.
    created = models.DateTimeField(auto_now_add = True)

    userpic= models.ForeignKey('filemanager.fileobject', blank=True, null=True, on_delete=models.SET_NULL , related_name='userpic')

    bio = models.CharField(max_length=256, blank=True,  default="I didn't really care to tell you about myself, so the developers wrote this.")

    listpref = models.SmallIntegerField(max_length=256, blank=True, null=True,)

    def __unicode__(self):
        return str(self.user)+"Profile"



User.profile = property(lambda u: userProfile.objects.get_or_create(user=u)[0])
