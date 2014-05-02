from django.conf.urls.defaults import *
from django.contrib.admin.views.decorators import staff_member_required

from taggit_autocomplete.views import list_tags

urlpatterns = patterns('',
    url(r'^list/$', staff_member_required(list_tags),
        name='taggit_autocomplete-list'),
)
