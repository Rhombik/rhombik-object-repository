# Create your views here.

from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from blog.models import Post
from django.conf import settings
import os 


import thumbnailer


def galleryview(request,title):
    #print "request: "+str(request)+"\n"+"title: "+str(title)
    ###start directory walking
    images = []
    for i in os.walk(settings.MEDIA_ROOT+"uploads/" + title , topdown=True, onerror=None, followlinks=False):
        for z in i[2]:##If anyone doesn't know, the [2] is because 0 is dir, 1 is folders, and 2 is files.
           images.append(thumbnailer.thumbnail(i[0]+"/"+z,(64,64)))
            

    c = RequestContext(request, dict(post=Post.objects.filter(title=title)[0:1].get(), user=request.user, images=images, galleryname="gallery"))


    return render(request, "article.html", c)

def imagedownload(request, title):
    c = RequestContext(request, dict(post=Post.objects.filter(title=title)[0:1].get(), user=request.user, images=images))
    return render(request, "gallery.html", c) 

def stlthumb(request, path):
    c = RequestContext(request, dict(user=request.user, path=path))
    return render(request, "thumbs/stl.html", c)

def stlview(request, path):
    c = RequestContext(request, dict(user=request.user, path=path))
    return render(request, "filehandlers/stl.html", c)

