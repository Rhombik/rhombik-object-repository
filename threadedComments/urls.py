
from django.conf.urls import *
from django.conf import settings

#uhhhm, so theres nothing here. And maybe there never will be.
## if you want to use this place make sure you modify Settings/urls.py first...
urlpatterns = patterns("",
    (r'^project/(?P<content_pk>\d+)/comment/(?P<parent_id>\d+)/(?P<comment_id>.+)/$', 'threadedComments.views.comment', {'content_type':'project',}),
)
