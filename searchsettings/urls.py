from django.conf.urls import *
from haystack.views import search_view_factory
from searchsettings.views import SearchView
from searchsettings.forms import objectSearchForm


urlpatterns = patterns('haystack.views',
    url(r'^$', search_view_factory(
        view_class=SearchView,
        template='search/search.html',
        form_class=objectSearchForm
    ), name='haystack_search'),
)
