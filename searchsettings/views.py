# Create your views here.

from haystack.views import SearchView
from project.views import project_list_get

class SearchView(SearchView):
    def extra_context(self):
        projects = []
        for i in self.results:
            projects += [i.object]
        data = project_list_get(projects)
        return {
            'listdata': data,
        }
