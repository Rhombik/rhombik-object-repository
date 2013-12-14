
from project.models import *
from django.contrib import admin
try:
    from avatarBot.models import uploadPic, userPicThumb
except:
    from models import uploadPic, userPicThumb


class ProjectAdmin(admin.ModelAdmin):
    search_fields = ["title"]

admin.site.register(uploadPic)
admin.site.register(userPicThumb)
