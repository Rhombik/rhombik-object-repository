from django import template
from django.template.defaultfilters import stringfilter
from bs4 import BeautifulSoup,NavigableString
from filemanager.models import fileobject
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
                picture.insert(0, BeautifulSoup(render_to_string("gallery.html", dict(images=[[objectish.thumbname.url, objectish.filename.url, objectish.filetype]], galleryname=picture["galleryname"])), "html.parser"))
            except:
                picture.insert(0,"")
        html = soup #and now the value is html. My work here is done.
    else:
        html=value
    return html
