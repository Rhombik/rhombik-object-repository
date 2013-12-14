# Create your views here.

from filemanager.models import fileobject,thumbobject,zippedobject
from project.models import *
import os.path
from django.shortcuts import render_to_response, render


def download(request, pk):
    project = Project.objects.filter(pk=pk).exclude(draft=True)[0:1].get()
    projectfiles = fileobject.objects.filter(project=project)
    download=[]
    for i in projectfiles:
        thumbmodel=thumbobject.objects.get_or_create( fileobject = i, filex=64, filey=64 )[0]
        downloadlink=i.filename.url
        name=i.subfolder+os.path.split(i.filename.name)[1]
        thumbnail=thumbmodel.filename.url
        filetype=thumbmodel.filetype
        download.append([thumbnail,name,downloadlink,filetype])
 
    return render(request, "download.html", dict(download=download))


