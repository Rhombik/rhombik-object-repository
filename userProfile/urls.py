from django.conf.urls import patterns, url, include
from userProfile.views import *
urlpatterns = patterns('',
    url('^legister/', legister),
    url('^login/', legister),
    url('^logout/', logoutView),
    url(r'^userProfile/(.*)/$', index),
    url('^', include('django.contrib.auth.urls')),
)
