from project.models import *
from django.contrib import admin


class ProjectAdmin(admin.ModelAdmin):
    search_fields = ["title"]

admin.site.register(Project, ProjectAdmin)

