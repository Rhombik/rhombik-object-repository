from django.db import models
import thumbnailer.thumbnailer
from post.models import Post
# Create your models here.

class fileobject(models.Model):

    def uploadpath(instance, filename):
        return 'uploads/%s/%s/%s' % (instance.post_id, instance.subfolder, filename)


    post = models.ForeignKey(Post)
    subfolder = models.CharField(max_length=256, default="/")
    filename = models.FileField(upload_to=uploadpath)
    thumbnailpath = models.CharField(max_length=256, blank=True, null=True)
    filetype = models.CharField(max_length=60, blank=True, null=True)


    def save(self):
        super(fileobject, self).save()

        thumbnaildata = thumbnailer.thumbnailer.thumbnail(self.filename.path,(200,200), forceupdate=True)
        self.thumbnailpath = thumbnaildata[0]
        self.filetype = thumbnaildata[2]
        super(fileobject, self).save()

