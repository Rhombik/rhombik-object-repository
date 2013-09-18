
from django.db import models

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
import thumbnailer.thumbnailer2
import os

"""  uploadPic holds the users uploaded profile picture  """
class uploadPic(models.Model):

    user = models.ForeignKey(User, unique=True)
    filename = models.ImageField(upload_to="userPics/", null=True)
    profilePicType = models.CharField(max_length=64, blank=True, null=True)

    def __unicode__(self):
        return str(self.user)+"ProfilePic"

    def save(self, force_insert=False, force_update=False, using=None):
        super(uploadPic, self).save()

        thumbnaildata = userPicThumb.objects.get_or_create(pic = self, filex = 64, filey = 64)[0]
        
        self.profilePicType = thumbnaildata.filetype

        self.user.profile.avatarType = "upload"

        super(uploadPic, self).save()

    def delete(self, *args, **kwargs):
        super(uploadPic, self).delete(*args, **kwargs)
        default_storage.delete(self.filename)


"""  userPicThumb is different sized thumbnails of uploadPic  """
class userPicThumb(models.Model):

    #A pointer to the file this is a thumbnail of.
    pic = models.ForeignKey(uploadPic)

    #This is the actual thumbnail, stored using django storage, whatever that may be.
    thumb = models.FileField(upload_to="userPics/thumbs/", blank=True, null=True)

    #What the file type is
    filetype = models.CharField(max_length=60, blank=True, null=True)

    #the size of the file.
    filex = models.PositiveSmallIntegerField()
    filey = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('filex', 'filey', "thumb")

    def __unicode__(self):
        return str(self.pic)+"Thumb"

    def save(self, *args, **kwargs):
        self.thumb, self.filetype = thumbnailer.thumbnailer2.thumbnailify(self.pic, (self.filex, self.filey))
        super(userPicThumb, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(userPicThumb, self).delete(*args, **kwargs)
        default_storage.delete(self.thumb)

