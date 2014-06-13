from django.db import models
from thumbnailer import thumbnailer2
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from io import BytesIO
import os.path
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class fakefile():
    url = ""
#    def url():
#        return("null")

# Create your models here.

class fileobject(models.Model):
    def uploadpath(instance, filename):
        return ("uploads/"+str(instance.object_id)+instance.subfolder+filename)

## These attributes point to the object/project/userProfile that this file belongs to.
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    parent = generic.GenericForeignKey('content_type', 'object_id')

    subfolder = models.CharField(max_length=256, default="/")
    filename = models.FileField(upload_to=uploadpath,null=True)
    filetype = models.CharField(max_length=16, blank=True, null=True, default="norender")


### I don't know why __unicode__() broke, but unicode() fixed it... so now we have both.
    def unicode(self):
        return str(self.filename)
    def __unicode__(self):
        return str(self.filename)
    def get_thumb(self, sizex, sizey):
        thumbmodel=thumbobject.objects.get_or_create(fileobject = self, filex=sizex, filey=sizey )[0]
        renderer = str(thumbmodel.filetype)
        if renderer != "ajax" or "norender" or "":
            return [thumbmodel,self,renderer]
        elif (renderer == "ajax"):
            return ["",self,self.renderer]
        else:
            return


    def save(self):
        super(fileobject, self).save()
        self.filetype = thumbnailer2.thumbnailify(self, (1,1))[1]
        super(fileobject, self).save()

    def delete(self, *args, **kwargs):
        from project.tasks import ThumbnailEnforcer
        self.filename.delete()
        super(fileobject, self).delete(*args, **kwargs)
        #parent does not need to implement an enf_consistancy method. It is optional.
        try:
            self.parent.enf_consistancy()
        except:
            pass

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

    def __unicode__(self):
        return str(self.filename)
    
    class Meta:
        unique_together = ('filex', 'filey', "fileobject")

#        index_together = [['filex', 'filey', "fileobject"]]
    def save(self, generate=True, *args, **kwargs):
        if generate == True:
            self.filetype = "ajax"

        super(thumbobject, self,).save()
        if generate == True:
            from filemanager.tasks import thumbTask
            thumbTask.delay(self, self.fileobject)

    def delete(self, *args, **kwargs):
        import warnings
        try:
            self.filename.delete()
        except:
            pass
        super(thumbobject, self).delete(*args, **kwargs)


class zippedobject(models.Model):

    def __unicode__(self):
        return str(self.project.title)

    project = models.ForeignKey('project.Project', unique=True)
    filename = models.FileField(upload_to="projects/", blank=True, null=True)
    def save(self, generate=True, *args, **kwargs):
        super(zippedobject, self).save()
        if generate == True:
            from filemanager.tasks import zippedTask
            zippedTask(self, self.project)

    def delete(self, *args, **kwargs):
        import warnings
        try:
            self.filename.delete()
        except:
            pass


import thumbnailer.shadowbox
import markdown

class htmlobject(models.Model):

    def __unicode__(self):
        return str(self.fileobject.filename)
    #A pointer to the file this is a thumbnail of.
    fileobject = models.ForeignKey(fileobject, unique=True)
    body_rendered = models.TextField('Entry body as HTML', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.body_rendered = markdown.markdown(self.fileobject.filename.read(), safe_mode=True)
        super(htmlobject, self).save(*args, **kwargs)

