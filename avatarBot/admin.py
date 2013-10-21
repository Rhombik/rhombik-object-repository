
from post.models import *
from django.contrib import admin
from avatarBot.models import uploadPic, userPicThumb

class PostAdmin(admin.ModelAdmin):
    search_fields = ["title"]

admin.site.register(uploadPic)
admin.site.register(userPicThumb)
