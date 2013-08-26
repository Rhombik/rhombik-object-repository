from filemanager.models import *
from django.contrib import admin


class fileobjectAdmin(admin.ModelAdmin):
    search_fields = ["post"]

admin.site.register(fileobject,fileobjectAdmin)

