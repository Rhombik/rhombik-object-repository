from django.http import HttpResponseRedirect#, HttpResponse
from scraper.forms import ImportForm
from scraper.tasks import scrapeTask


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
    return HttpResponseRedirect('/mydrafts/')

