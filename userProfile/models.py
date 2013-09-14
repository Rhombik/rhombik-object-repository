from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import thumbnailer.thumbnailer2
import os
from django.conf import settings

# Create your models here.

class userProfile(models.Model):

    user = models.ForeignKey(User, unique=True)

    ###this to be replaced when I figure out how to grab date created from user
    created = models.DateTimeField(auto_now_add = True)

    #username = models.CharField(max_length=30, blank=True, null=True)
    filename = models.FileField(upload_to="userPics/", null=True)
    profilePicType = models.CharField(max_length=64, blank=True, null=True)
    bio = models.CharField(max_length=256, blank=True,  default="I didn't really care to tell you about myself, so the developers wrote this.")
    email = models.EmailField(blank=True, null=True)

    def __unicode__(self):
        return str(self.user)+"Profile"

    def save(self, force_insert=False, force_update=False, using=None):
        super(userProfile, self).save()

        thumbnaildata = userpicthumb.objects.get_or_create(fileobject = self, filex = 64, filey = 64)[0]
        
        self.profilePicType = thumbnaildata.filetype

        super(userProfile, self).save()


########         Alll of this is Evil, and will be erased once tristan is sure everyting works without it.     #####    
#   def save(self, force_insert=False, force_update=False, using=None):##def save(self):
#       super(userProfile, self).save()
#      #self.filename = fileishness#request.FILES["filename"]
#      #self.filename.save(str(self.user.username)+"Pic.png", fileishness)
#       if not self.filename=="stoopid":
#           try:
#               thumbnaildata = thumbnailer.thumbnailer.thumbnail(self.filename.path,(200,200), forceupdate=True)
#               self.profilePicType=thumbnaildata[2]
#               self.profilePicPath=thumbnaildata[1]
#               self.profilePicThumb=thumbnaildata[0]
#           except:
#               self.profilePicThumb=settings.URL+"/static/noUserPic.png"
#               self.profilePicPath=settings.URL+"/static/noUserPic.png"
#               self.profilePicType="browser"
#               self.filename="stoopid"
#       super(userProfile, self).save()

##The save function stolen from filemanager.models.fileobject, for setting the default thumb.
#    def save(self):

#      #try:
#        thumbnaildata = thumbnailer2.thumbnailify(self, (128,128))
#        self.thumbname = thumbnaildata[0]
#        self.filetype = thumbnaildata[1]
#      #except:
#      #    self.filetype = "norender"
#        super(fileobject, self).save()

#    def delete(self, *args, **kwargs):
#        super(fileobject, self).delete(*args, **kwargs)
#        default_storage.delete(self.filename)
#        default_storage.delete(self.thumbname)

class userpicthumb(models.Model):
    #A pointer to the file this is a thumbnail of.
    fileobject = models.ForeignKey(userProfile)
    #This is the actual thumbnail, stored using django storage, whatever that may be.
    filename = models.FileField(upload_to="userPics/thumbs/", blank=True, null=True)
    #What the file type is
    filetype = models.CharField(max_length=60, blank=True, null=True)
    #the size of the file.
    filex = models.PositiveSmallIntegerField()
    filey = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('filex', 'filey', "fileobject")

    def save(self, *args, **kwargs):
        #try:
##           old thumbnailer
#            thumbnaildata = thumbnailer.thumbnailer.thumbnail(self.filename.path,(128,128), forceupdate=True)
        print("self.fileobject is "+str(self.fileobject))
        self.filename, self.filetype = thumbnailer.thumbnailer2.thumbnailify(self.fileobject, (self.filex, self.filey))
        #except:
        #    self.filetype = "norender"
        super(userpicthumb, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(thumbobject, self).delete(*args, **kwargs)
        default_storage.delete(self.filename)



User.profile = property(lambda u: userProfile.objects.get_or_create(user=u)[0])
