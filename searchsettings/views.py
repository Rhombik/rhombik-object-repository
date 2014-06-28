# Create your views here.

from haystack.views import SearchView
from project.views import project_list_get

class SearchView(SearchView):
    def extra_context(self):
#        listdata = project_list_get(self.results)
        paginator, page = self.build_page()


        print(page)
        return {
            'yourValue': "yourValue",
        }
