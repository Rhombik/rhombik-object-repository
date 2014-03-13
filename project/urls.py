from django.conf.urls import *
from django.conf import settings

urlpatterns = patterns("",

    (r'^project/(.*)/$', 'project.views.project'),

)
