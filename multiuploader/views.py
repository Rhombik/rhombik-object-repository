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
log = logging

from multiuploader.forms import MultiuploaderImage
from post.models import *


@csrf_exempt
def multiuploader_delete(request, pk):
    """
    View for deleting photos with multiuploader AJAX plugin.
    made from api on:
    https://github.com/blueimp/jQuery-File-Upload
    """
    if request.method == 'POST':
        log.info('Called delete image. image id='+str(pk))
        image = get_object_or_404(MultiuploaderImage, pk=pk)
        image.delete()
        log.info('DONE. Deleted photo id='+str(pk))
        return HttpResponse(str(pk))
    else:
        log.info('Received not POST request to delete image view')
        return HttpResponseBadRequest('Only POST accepted')

@csrf_exempt
def multiuploader(request,title):
    """
    Main Multiuploader module.
    Parses data from jQuery plugin and makes database changes.
    """
    if request.method == 'POST':
        log.info('received POST to main multiuploader view')
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')

        #getting file data for farther manipulations
        file = request.FILES[u'files[]']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size
        log.info ('Got file: "%s"' % str(filename))


        #Writing file to disk
        filepath = settings.MEDIA_ROOT+"uploads/"+title+"/"+filename
        print("filepath: "+filepath)
        path = default_storage.save(filepath, ContentFile(file.read())) 


        #getting thumbnail url using sorl-thumbnail
        thumbnailstring = thumbnailer.thumbnailer.thumbnail(filepath, (64,64), forceupdate=True)
        thumb_url = thumbnailstring[0]
        file_url = thumbnailstring[1]
        #settings imports
        try:
            file_delete_url = settings.MULTI_FILE_DELETE_URL+'/'
            file_url = path
        except AttributeError:
            file_delete_url = 'multi_delete/'
            file_url = path

        #generating json response array
        result = []
        result.append({"name":filename, 
                       "size":file_size, 
                       "url":file_url, 
                       "thumbnail_url":thumb_url,
                       "delete_url":file_delete_url+str(path), 
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
        images = []
        for i in os.walk(settings.MEDIA_ROOT+"uploads/" + title +"/", topdown=True, onerror=None, followlinks=False):
            for z in i[2]:##If anyone doesn't know, the [2] is because 0 is dir, 1 is folders, and 2 is files.
                filename = i[0]+z
                print (filename)
                images.append(thumbnailer.thumbnailer.thumbnail(filename,(64,64)))
        file_delete_url = settings.MULTI_FILE_DELETE_URL+'/'
        result = []
        for image in images:
            thumb_url = image[0]
            file_url = image[1]
            ##json stuff
            result.append({"name":"name",
                       "size":"size",
                       "url":file_url,
                       "thumbnail_url":thumb_url,
                       "delete_url":file_delete_url+str(file_url)+'/',
                       "delete_type":"POST",})
        response_data = simplejson.dumps(result)

        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, mimetype=mimetype)


def multi_show_uploaded(request, title):
    """Simple file view helper.
    Used to show uploaded file directly"""
    post=Post.objects.filter(title=title)[0:1].get()
    thumbnailstring = thumbnailer.thumbnailer.thumbnail(filepath, (64,64))
    url = thumbnailstring[0]
    print("adding \""+url+"\" to url string")
    return render_to_response('multiuploader/one_image.html', {"multi_single_url":url,})
