# Create your views here.

from filemanager.models import fileobject,thumbobject,zippedobject
from project.models import *
import os.path
from django.shortcuts import render_to_response, render
from django.http import HttpResponse


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

def ajaxthumblist(request,csv):
    from filemanager.models import thumbobject
    import json
    csv = csv.split(',')
    jsondata= []
    for i in csv:
        localdata = [{"pk":int(i)}]
        try:
            thumbinstance = thumbobject.objects.get(pk=int(i))
        except:
            thumbinstance= False
            localdata.append({"error":"404"})

        if thumbinstance != False:
            if thumbinstance.filetype == "norender" or thumbinstance.filetype == "text":
                localdata.append({"error":"Not a thumbnailable data type"})
            elif not thumbinstance.filename:
                localdata.append("loading")
                localdata.append({"size":(thumbinstance.filex,thumbinstance.filey)})
            elif thumbinstance.filename.url:
                localdata.append({"html":str(thumbinstance.filename.url)})
                localdata.append({"size":(thumbinstance.filex,thumbinstance.filey)})


        jsondata.append({"object":localdata})

    response_data = json.dumps(jsondata,sort_keys=True,
                  indent=4, separators=(',', ': '))


    if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
        mimetype = 'application/json'
    else:
        mimetype = 'text/plain'
    return HttpResponse(response_data, mimetype=mimetype)


