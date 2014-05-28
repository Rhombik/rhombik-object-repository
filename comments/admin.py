
from comments.models import *
from mptt.admin import MPTTModelAdmin
from django.contrib import admin

class CommentRootAdmin(MPTTModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('parent', 'content_type', 'object_id'),
            'description' : ("Warning: Parent probably shouldn't be set for comment roots. Please just leave this alone."),
        }),
    )

admin.site.register(CommentRoot, CommentRootAdmin)
admin.site.register(Comment, MPTTModelAdmin)
