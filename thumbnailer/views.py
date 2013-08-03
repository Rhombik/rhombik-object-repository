# Create your views here.

from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.conf import settings
import os 


import thumbnailer



def imagedownload(request, title):
    c = RequestContext(request, dict(post=Post.objects.filter(title=title)[0:1].get(), user=request.user, images=images))
    return render(request, "gallery.html", c) 

def stlthumb(request, path):
    c = RequestContext(request, dict(user=request.user, path=path))
    return render(request, "thumbs/stl.html", c)

def stlview(request, path):
    c = RequestContext(request, dict(user=request.user, path=path))
    return render(request, "filehandlers/stl.html", c)

