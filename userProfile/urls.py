from django.conf.urls import patterns, url, include
from userProfile.views import *
urlpatterns = patterns('',
    url('^', include('django.contrib.auth.urls')),
    url('^legister/', legister),
    url('^login/', legister)
)
