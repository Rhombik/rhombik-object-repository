from django.http import HttpResponseRedirect#, HttpResponse
from scraper.forms import ImportForm
from scraper.tasks import scrapeTask
from django.shortcuts import get_object_or_404, render_to_response
from multiuploader.views import draftview

def importer(request):
    ###Write a scraper dispatcher here.
    if request.method == 'POST':
        form = ImportForm(request.POST.copy())
        if form.is_valid() and request.user.is_authenticated():
            user=request.user
            print("THE USER IS:::")
            print(user)
            urls=[form.cleaned_data['url']]
            scrapeTask.delay(urls, user)
    return draftview(request, scraperMessage=True)
    #return HttpResponseRedirect('/mydrafts/', c)

