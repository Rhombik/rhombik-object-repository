# Create your views here.

def importer(request, pk):
    ###Write a scraper dispatcher here.
    c = RequestContext(request, dict())
    return render(request, "article.html", c)

