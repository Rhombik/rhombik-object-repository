from django.conf.urls import *
from django.conf import settings


urlpatterns = patterns('',
    (r'^download/(.*)/$', 'filemanager.views.download'),
    (r'^ajax/thumblist/(.*)/$', 'filemanager.views.ajaxthumblist', {'template': 'gallery.html'}),
)
