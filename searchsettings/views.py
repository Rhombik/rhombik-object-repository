# Create your views here.

from haystack.views import SearchView


class SearchView(SearchView):
    def extra_context(self):
        print("list of page objects")
        print(page.object_list)
        print("---------------\n")
        return {
            'yourValue': "yourValue",
        }
