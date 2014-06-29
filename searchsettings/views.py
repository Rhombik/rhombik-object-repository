# Create your views here.

from haystack.views import SearchView
from project.views import project_list_get

class SearchView(SearchView):
    def extra_context(self):
#        listdata = project_list_get(self.results)
        paginator, page = self.build_page()

        objectList=[]
        for i in page.object_list:
            objectList.append(i.object)
        
        print(objectList)

        listdata=project_list_get(objectList)
        print(listdata)
        return {
            'listdata': listdata,
        }
