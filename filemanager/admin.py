from filemanager.models import *
from django.contrib import admin
from django.contrib.contenttypes import generic

class fileobjectInline(generic.GenericTabularInline):
    model = fileobject
    extra = 0

class fileobjectAdmin(admin.ModelAdmin):
    search_fields = ["project"]

admin.site.register(fileobject,fileobjectAdmin)

class zippedobjectAdmin(admin.ModelAdmin):
    search_fields = ["project"]

admin.site.register(zippedobject,zippedobjectAdmin)

class thumbobjectAdmin(admin.ModelAdmin):
    list_filter = ('filetype',)
    list_display = ["fileobject",'filename', 'filetype', 'filex', 'filey'] 

admin.site.register(thumbobject,thumbobjectAdmin)


class htmlobjectAdmin(admin.ModelAdmin):
    search_fields = ["fileobject"]

admin.site.register(htmlobject,htmlobjectAdmin)

