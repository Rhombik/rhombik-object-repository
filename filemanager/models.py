from django.db import models
import thumbnailer.thumbnailer

# Create your models here.

class filename(models.Model):

    filename = models.FileField(upload_to="userPics/")
    thumbnailpath = models.CharField(max_length=256, blank=True, null=True)
    filetype = models.CharField(max_length=60, blank=True, null=True)
    def save(self):
        thumbnaildata = thumbnailer.thumbnailer.thumbnail(self.filename,(200,200), forceupdate=True)
        self.thumbnailpath = thumbnaildata[0]
        self.filetype = thumbnaildata[2]
        super(filename, self).save()

