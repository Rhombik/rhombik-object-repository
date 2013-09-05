from django import template
from django.template.defaultfilters import stringfilter
from bs4 import BeautifulSoup,NavigableString
from filemanager.models import fileobject

register = template.Library()

@register.filter
@stringfilter
def gallerfy(value):
    soup = BeautifulSoup(''.join(value))
    galleries = soup.findAll("fileobject")
    newgallery = []
    for picture in galleries:
        objectish = fileobject.objects.filter(id=picture["id"])
        print(objectish)
        picture.insert(0,"look at this:  "+str(objectish.filename))
        print(picture["id"])
        newgallery.append(picture)
    print (soup)
    html = soup #and now the value is html. My work here is done.
    return html
