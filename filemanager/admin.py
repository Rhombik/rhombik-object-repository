from filemanager.models import *
from django.contrib import admin


class fileobjectAdmin(admin.ModelAdmin):
    search_fields = ["project"]


admin.site.register(fileobject,fileobjectAdmin)

class zippedobjectAdmin(admin.ModelAdmin):
    search_fields = ["project"]

admin.site.register(zippedobject,zippedobjectAdmin)

class thumbobjectAdmin(admin.ModelAdmin):
    search_fields = ["project"]

admin.site.register(thumbobject,thumbobjectAdmin)

