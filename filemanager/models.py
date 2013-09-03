from django.db import models
import thumbnailer.thumbnailer
from post.models import Post
from django.core.files.storage import default_storage
# Create your models here.

class fileobject(models.Model):

    def uploadpath(instance, filename):
        return ("uploads/"+str(instance.post.id)+instance.subfolder+filename)


    post = models.ForeignKey(Post)
    subfolder = models.CharField(max_length=256, default="/")
    filename = models.FileField(upload_to=uploadpath)
    previewurl = models.CharField(max_length=256, blank=True, null=True)
    thumbnailpath = models.CharField(max_length=256, blank=True, null=True)
    filetype = models.CharField(max_length=60, blank=True, null=True)


    def save(self):
        super(fileobject, self).save()
        try:
            thumbnaildata = thumbnailer.thumbnailer.thumbnail(self.filename.path,(128,128), forceupdate=True)
            self.thumbnailpath = thumbnaildata[0]
            self.previewurl = thumbnaildata[1]
            self.filetype = thumbnaildata[2]
        except:
            self.filetype = "norender"
        super(fileobject, self).save()
    def delete(self, *args, **kwargs):
        super(fileobject, self).delete(*args, **kwargs)
        default_storage.delete(self.filename)

class thumbobject(models.Model):
    #A pointer to the file this is a thumbnail of.
    fileobject = models.ForeignKey(fileobject)
    #This is the actual thumbnail, stored using django storage, whatever that may be.
    filename = models.FileField(upload_to="/thumbs/", blank=True, null=True)
    #What the file type is
    filetype = models.CharField(max_length=60, blank=True, null=True)
    #the size of the file.
    filex = PositiveSmallIntegerField()
    filey = PositiveSmallIntegerField()
    
    class Meta:
        unique_together = ('filex', 'filey',)

    super(fileobject, self).save()
        try:
##           old thumbnailer
#            thumbnaildata = thumbnailer.thumbnailer.thumbnail(self.filename.path,(128,128), forceupdate=True)
            thumbnaildata = thumbnail2(self.fileobject.filename.url ,(str(self.filex),str(self.filey)))
            self.filename = thumbnaildata[0]
            self.filetype = thumbnaildata[1]
        except:
            self.filetype = "norender"
        super(thumbobject, self).save()

    def delete(self, *args, **kwargs):
        super(thumbobject, self).delete(*args, **kwargs)
        default_storage.delete(self.filename)


 
