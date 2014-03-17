from django.conf.urls import *
from haystack.views import SearchView, search_view_factory
from searchsettings.forms import DateRangeSearchForm

urlpatterns = patterns('haystack.views',
    url(r'^$', search_view_factory(
        view_class=SearchView,
#        template='my/special/path/john_search.html',
        form_class=DateRangeSearchForm
    ), name='haystack_search'),
)
