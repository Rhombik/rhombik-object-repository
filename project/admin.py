from project.models import *
from django.contrib import admin
from filemanager.admin import fileobjectInline

class ProjectAdmin(admin.ModelAdmin):
    inlines = [fileobjectInline]
    search_fields = ["title"]
admin.site.register(Project, ProjectAdmin)

