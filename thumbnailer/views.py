# Create your views here.

from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.conf import settings
import os 


import thumbnailer
from filemanager.models import fileobject, thumbobject
from django.shortcuts import get_object_or_404


def stlthumb(request, path):
    objectish = get_object_or_404(fileobject, pk=path)
    c = RequestContext(request, dict(user=request.user, path=objectish.filename.url))
    return render_to_response("thumbs/stl.html", c)

def stlview(request, path):
    objectish = get_object_or_404(fileobject, pk=path)
    print(objectish)
    c = RequestContext(request, dict(user=request.user, path=objectish.filename.url))
    return render_to_response("filehandlers/stl.html", c)

