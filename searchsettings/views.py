# Create your views here.

from haystack.views import SearchView
from searchsettings.forms import DateRangeSearchForm 


class SearchView(SearchView):
    form_class = DateRangeSearchForm
