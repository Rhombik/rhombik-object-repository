# Create your views here.

from filemanager.models import fileobject,thumbobject,zippedobject
from project.models import *
import os.path
from django.shortcuts import render_to_response, render
from django.http import HttpResponse


def download(request, pk):
    project = Project.objects.filter(pk=pk).exclude(draft=True)[0:1].get()
    object_type = ContentType.objects.get_for_model(project)
    projectfiles = fileobject.objects.filter(content_type=object_type,object_id=project.id)
    download=[]
    for i in projectfiles:
        thumbmodel=thumbobject.objects.get_or_create( fileobject = i, filex=64, filey=64 )[0]
        downloadlink=i.filename.url
        name=i.subfolder+os.path.split(i.filename.name)[1]
        try:
            thumbnail=thumbmodel.filename.url
        except:
            thumbnail=None
        filetype=thumbmodel.filetype
        download.append([thumbnail,name,downloadlink,filetype,i])
 
    return render(request, "downloadWrapper.html", dict(download=download))

def ajaxthumblist(request,csv,template):
    from filemanager.models import thumbobject
    import json
    csv = csv.rstrip(',').split(',')
    jsondata= []
    for i in csv:
        localdata = {"pk":int(i)}
        try:
            thumbinstance = thumbobject.objects.get(pk=int(i))
        except:
            thumbinstance= False
            localdata["error"] = "404"

        if thumbinstance != False:
            if thumbinstance.filetype == "norender" or thumbinstance.filetype == "text" or not thumbinstance.filetype:
                localdata["error"] = "Not a thumbnailable data type"
            elif not thumbinstance.filename and thumbinstance.filetype == "ajax":
                localdata["loading"] = True
                localdata["size"] =(thumbinstance.filex,thumbinstance.filey)
            elif thumbinstance.filename.url:
                from django.template.loader import render_to_string
    
                images=[thumbinstance.fileobject.get_thumb(thumbinstance.filex,thumbinstance.filey)]
                rendered = render_to_string(template, dict(images=images, galleryname="ajax"))
                rendered = rendered.strip('\n')
                localdata["html"] = str(rendered)
                localdata["size"] = (thumbinstance.filex,thumbinstance.filey)


        jsondata.append(localdata)

    response_data = json.dumps(jsondata,sort_keys=True,
                  indent=4, separators=(',', ': '))


    if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
        mimetype = 'application/json'
    else:
        mimetype = 'text/plain'
    return HttpResponse(response_data, mimetype=mimetype)


