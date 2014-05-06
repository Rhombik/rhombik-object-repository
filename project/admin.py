from project.models import *
from django.contrib import admin
from filemanager.admin import fileobjectAdmin

class ProjectAdmin(admin.ModelAdmin):
    search_fields = ["title"]
admin.site.register(Project, ProjectAdmin)

