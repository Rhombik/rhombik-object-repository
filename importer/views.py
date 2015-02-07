from django.http import HttpResponseRedirect#, HttpResponse
from importer.forms import ImportForm
from importer.tasks import ThingiProjectTask,ThingiUserTask
from django.shortcuts import get_object_or_404, render_to_response
from multiuploader.views import draftview

import re
''' nifty parse function performs all the identification that can be done on a url without making any get requests. It returns a good value, and if True, a task to call, or False and an error message '''
def parse(url):
    if re.search('thingiverse\.com',url):
        #gee wiz, it's from thiniverse!
	if re.search('thing:\d\d+',url):#it's a thing/project page
            return(True,ThingiProjectTask)
        else:
	    return(True,ThingiUserTask)#it's probably a user page. or it's another page, but we aren't checking that here.
    else:
	return(False,"Unknown Domain")

def importer(request):
    ###Write a scraper dispatcher here.
    if request.method == 'POST':
        form = ImportForm(request.POST.copy())
        if form.is_valid() and request.user.is_authenticated():
            user=request.user
            url=form.cleaned_data['url']
	    good,kind=parse(url)
	    if good:
                kind.delay(url, user)
	    else:
	        # neeto unknown site error! these should prolly get logged.
		pass
	##else we need to be giving them shiny errors as to why it isn't valid.
    return draftview(request, scraperMessage=True)
    #return HttpResponseRedirect('/mydrafts/', c)

