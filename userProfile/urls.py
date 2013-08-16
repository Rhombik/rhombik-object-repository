from django.conf.urls import patterns, url

from userProfile import views

urlpatterns = patterns('',
    url(r'^(.*)/$', views.index, name='index')
)
