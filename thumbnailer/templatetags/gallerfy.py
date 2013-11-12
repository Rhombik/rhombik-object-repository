from django import template
from django.template.defaultfilters import stringfilter
from bs4 import BeautifulSoup,NavigableString
from filemanager.models import fileobject, thumbobject
from django.shortcuts import get_object_or_404, render_to_response
from django.template.loader import render_to_string


register = template.Library()

@register.filter
@stringfilter
def gallerfy(value):
    soup = BeautifulSoup(value, "html.parser")
    galleries = soup.findAll("fileobject")
    if galleries:
        for picture in galleries:
            try:
                objectish = get_object_or_404(fileobject, pk=picture["id"])
                thumb = thumbobject.objects.get_or_create(fileobject = objectish, filex = 64, filey = 64)[0]
                picture.insert(0, BeautifulSoup(render_to_string("gallery.html", dict(images=[[thumb.filename.url, objectish.pk, objectish.filetype]], galleryname=picture["galleryname"])), "html.parser"))
            except:
                picture.insert(0,"")
    return soup
