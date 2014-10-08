from django.http import HttpResponseRedirect#, HttpResponse
from spider.spiders.thingiverse import runScraper
from scraper.forms import ImportForm

def importer(request):
    ###Write a scraper dispatcher here.
    if request.method == 'POST':
        form = ImportForm(request.POST.copy())
        if form.is_valid() and request.user.is_authenticated():
            user=request.user
            print("THE USER IS:::")
            print(user)
            urls=[form.cleaned_data['url']]
            runScraper(urls, user=user)
    return HttpResponseRedirect('/mydrafts/')

