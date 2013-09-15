from django.db import models
from thumbnailer import thumbnailer2
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import zipfile
from io import BytesIO
import os.path
from django.core.files.uploadedfile import InMemoryUploadedFile


# Create your models here.

class fileobject(models.Model):

    def uploadpath(instance, filename):
        return ("uploads/"+str(instance.post.id)+instance.subfolder+filename)


    post = models.ForeignKey('post.Post')
    subfolder = models.CharField(max_length=256, default="/")
    filename = models.FileField(upload_to=uploadpath)
    filetype = models.CharField(max_length=16, blank=True, null=True)


    def __unicode__(self):
        return str(self.filename)


    def save(self):
        super(fileobject, self).save()

        thumbnaildata = thumbobject.objects.get_or_create(fileobject = self, filex = 64, filey = 64)[0]
        
        self.filetype = thumbnaildata.filetype

        super(fileobject, self).save()

    def delete(self, *args, **kwargs):
        super(fileobject, self).delete(*args, **kwargs)
        default_storage.delete(self.filename)
       #default_storage.delete(self.thumbname)


class thumbobject(models.Model):
    #A pointer to the file this is a thumbnail of.
    fileobject = models.ForeignKey(fileobject)
    #This is the actual thumbnail, stored using django storage, whatever that may be.
    filename = models.FileField(upload_to="thumbs/", blank=True, null=True)
    #What the file type is
    filetype = models.CharField(max_length=16, blank=True, null=True)
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
        self.filename, self.filetype = thumbnailer2.thumbnailify(self.fileobject, (self.filex, self.filey))
        #except:
        #    self.filetype = "norender"
        super(thumbobject, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(thumbobject, self).delete(*args, **kwargs)
        default_storage.delete(self.filename)




class zippedobject(models.Model):

    post = models.ForeignKey('post.Post', unique=True)
    filename = models.FileField(upload_to="projects/", blank=True, null=True)
    def save(self, *args, **kwargs):
        s = BytesIO()

        data = zipfile.ZipFile(s,'a')
        postfiles = fileobject.objects.filter(post=self.post)
        for filedata in postfiles:
            print(filedata.filename.name)
            filed = filedata.filename.read()
            pathAndName = str(self.post.title)+filedata.subfolder+os.path.split(str(filedata.filename))[1] #### this is where subfolders will be added to inside the zip file.
            data.writestr(pathAndName, filed)
        data.close()

        self.filename = InMemoryUploadedFile(s, None, self.post.title+".zip", '',
                                    1, None)
        super(zippedobject, self).save(*args, **kwargs)


