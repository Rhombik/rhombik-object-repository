# Create your views here.

from haystack.views import SearchView
from project.views import project_list_get
from searchsettings.forms import objectSearchForm

class SearchView(SearchView):
    def extra_context(self):
        projects = []
        for i in self.results:
            projects += [i.object]
        data = project_list_get(projects)

##I've heard tell of worse code. The big problem here is we don't know what variables we're going to have, and we don't just the content anyway.
#Would probably be a lot cleaner if I threw in a fre try statements...
        ##Set up the sort options, and current
        sortoptions=list(objectSearchForm.sortOPTIONS)
        if self.request.GET.get("sort", False):
            success=False
            for i in objectSearchForm.sortOPTIONS:
                if i[0] == self.request.GET["sort"]:
                   ordersortCurrent=i
                   sortoptions.remove(i)
                   success=True
                   break
            if success==False:
                ordersortCurrent=objectSearchForm.sortOPTIONS[0]
                sortoptions.remove(objectSearchForm.sortOPTIONS[0])
        else:
            ordersortCurrent=objectSearchForm.sortOPTIONS[0]
            sortoptions.remove(objectSearchForm.sortOPTIONS[0])

        ##Set up the time options, and current
        timeoptions=list(objectSearchForm.timeOPTIONS)
        if self.request.GET.get("From", False):
            success=False
            for i in objectSearchForm.timeOPTIONS:
                if i[0] == self.request.GET["From"]:
                   timesortCurrent=i
                   timeoptions.remove(i)
                   success=True
                   break
            if success==False:
                timesortCurrent=objectSearchForm.timeOPTIONS[0]
                timeoptions.remove(objectSearchForm.timeOPTIONS[0])
        else:
            timesortCurrent=objectSearchForm.timeOPTIONS[0]
            timeoptions.remove(objectSearchForm.timeOPTIONS[0])


        clean_url_dict=self.request.GET.copy()
        try:
            del clean_url_dict["sort"]
        except:
            pass
        try:
            del clean_url_dict["From"]
        except:
            pass
        cleaned_url = clean_url_dict.urlencode()
        return {
            "cleaned_url": cleaned_url,
            'listdata': data,
             "ordersort": {
                 "current": ordersortCurrent,
                 "options": sortoptions
             },
             "fromtime": {
                 "current": timesortCurrent,
                 "options": timeoptions
             }

        }
