from django.conf.urls import *
from django.conf import settings

urlpatterns = patterns("",
    (r'^gitTest/$', 'gitHooks.views.register'),
    (r'^githubOAuth/$', 'gitHooks.views.callback'),
)
