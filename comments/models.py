
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group

class Comment(MPTTModel):

    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    commenttext = models.CharField(max_length=4096)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    commenter = models.ForeignKey(User, related_name='commenter',default=User)

   ## This stuff is the content type, id, and ForeignKey of the object we are commenting on.
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    subject = generic.GenericForeignKey('content_type', 'object_id')

    
    def __str__(self):
        if(len(self.commenttext)>32):
            return str(self.commenttext[:32]+"... .. .")
        else:
            return str(self.commenttext)
