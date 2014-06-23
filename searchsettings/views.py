# Create your views here.

from haystack.views import SearchView


class SearchView(SearchView):
    def extra_context(self):
        return {
            'yourValue': "yourValue",
        }
