from organization.models import *
from django.contrib import admin


class orgAdmin(admin.ModelAdmin):
    search_fields = ["org_name"]
class clusterAdmin(admin.ModelAdmin):
    search_fields = ["organization"]


admin.site.register(org, orgAdmin)
admin.site.register(cluster,clusterAdmin)

