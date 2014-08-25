from django.shortcuts import get_object_or_404, render_to_response
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest

##from multiuploader.models import MultiuploaderImage
from django.core.files.uploadedfile import UploadedFile

#importing json parser to generate jQuery plugin friendly json response
from django.utils import simplejson

#for generating thumbnails
#sorl-thumbnails must be installed and properly configured
#from sorl.thumbnail import get_thumbnail

from django.views.decorators.csrf import csrf_exempt

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import thumbnailer.thumbnailer as thumbnailer

import logging
import os.path
from multiuploader.forms import MultiuploaderImage
from project.models import *
from filemanager.models import fileobject, thumbobject
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.shortcuts import redirect
from project.views import project_list_get
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.core.context_processors import csrf

def draftview(RequestContext):
    request = RequestContext
    projects = Project.objects.filter(author=int(request.user.id), draft=True)
    toomanydrafts = False
    if projects.count() > 8:
        toomanydrafts = True
    listdata = project_list_get(projects, purge=False)
    c = dict(toomanydrafts = toomanydrafts, listdata=listdata, user=request.user, active="home",)
    c.update(csrf(request))
    if projects:
        return render_to_response("drafts.html", c)
    else:
        return redirect("/create/")


@csrf_exempt
def multiuploader_delete(request, pk):
    """
    View for deleting photos with multiuploader AJAX plugin.
    made from api on:
    https://github.com/blueimp/jQuery-File-Upload
    """
    image = get_object_or_404(fileobject, pk=pk)
    project = image.parent


    if request.method == 'POST' and str(project.author) == str(request.user):
        log.info('Called delete image. image id='+str(pk))
        image.delete()
        log.info('DONE. Deleted photo id='+str(pk))
        return HttpResponse(str(pk))
    elif request.method == 'POST' and str(project.author) != str(request.user):
        log.info("user "+str(request.user)+" tried to delete object "+str(pk)+" which doesn't belong to them")
        return HttpResponse(status=403)
    else:
        log.info('Received not POST request to delete image view')
        return HttpResponseBadRequest('Only POST accepted')

@csrf_exempt
def multiuploader(request, pk):

    project=Project.objects.filter(pk=pk)[0]
    """
    Main Multiuploader module.
    Parses data from jQuery plugin and makes database changes.
    """
    if request.method == 'POST' and str(project.author) == str(request.user):
        log.info('received POST to main multiuploader view')
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')

        #getting file data for farther manipulations
        projectfiles = fileobject(parent=project)
      # projectfiles.project = project # this is nonsense... is this not nonsense? Cruft.
        projectfiles.filename = request.FILES[u'files[]']
        projectfiles.save()
        projectfiles.filename.close()

        log.info ('Got file: "%s"' % str(projectfiles.filename.name))


        #settings imports
        try:
            file_delete_url = settings.MULTI_FILE_DELETE_URL+'/'
        except AttributeError:
            file_delete_url = 'multi_delete/'
        #thumbnail = thumbobject.objects.get_or_create( fileobject = projectfiles, filex=64, filey=64 )[0]
        result = []
        ##It waits for the thumbnail to generate before sending the json, which should work.
        images=[projectfiles.get_thumb(64,64)]
        thumburl = render_to_string("gallery.html", dict(images=images, galleryname="ajax"))


        result.append({"name":projectfiles.subfolder+os.path.split(str(projectfiles.filename.name))[1], 
                       "size":projectfiles.filename.size, 
                       "thumbnail_url":thumburl,
                       "delete_url":"/multi_delete/"+str(projectfiles.pk)+"/", 
                       "delete_type":"POST",})
        response_data = simplejson.dumps(result)
        
        #checking for json data type
        #big thanks to Guy Shapiro
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, mimetype=mimetype)
    else: #GET
        object_type = ContentType.objects.get_for_model(project)
        projectfiles = fileobject.objects.filter(content_type=object_type,object_id=project.id)
  
        file_delete_url = settings.MULTI_FILE_DELETE_URL+'/'
        result = []
        for image in projectfiles:
            #thumbnail =  thumbobject.objects.get_or_create( fileobject = image, filex=64, filey=64 )[0]
            images=[image.get_thumb(64,64)]
            thumburl = render_to_string("gallery.html", dict(images=images, galleryname="ajax"))
            ##json stuff
            result.append({"name":image.subfolder+os.path.split(image.filename.name)[1],
                       "size":image.filename.size,
                       "thumbnail_url":thumburl,
                       "delete_url":"/multi_delete/"+str(image.pk)+"/",
                       "delete_type":"POST",})
        response_data = simplejson.dumps(result)
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, mimetype=mimetype)


