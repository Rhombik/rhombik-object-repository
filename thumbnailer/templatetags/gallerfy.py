from django import template
from django.template.defaultfilters import stringfilter
from bs4 import BeautifulSoup,NavigableString

register = template.Library()

@register.filter
@stringfilter
def gallerfy(value):
    soup = BeautifulSoup(''.join(value))
    galleries = soup.findAll("fileobject")
    newgallery = []
    print (galleries)
    for picture in galleries:
        print("picture is "+str(picture))
        picture.insert(0,"pisizicture!")
        print("picture is "+str(picture))
        newgallery.append(picture)
    print (newgallery)
    html = value #and now the value is html. My work here is done.
    return html
