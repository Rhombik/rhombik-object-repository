from os import path

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render

from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie

import thumbnailer.thumbnailer as thumbnailer 


from filemanager.models import fileobject, thumbobject, htmlobject, zippedobject, thumbObjectProxy

from project.models import Project
from project.forms import ProjectForm, createForm, defaulttag
from django import forms



"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
##obviously ignoring csrf is a bad thing. Get this fixedo.
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
from django.views.decorators.csrf import csrf_exempt, csrf_protect,requires_csrf_token
from django.core.context_processors import csrf


from django.http import HttpResponseRedirect, HttpResponse
from filemanager.models import fileobject

def searchtest(*args, **kwargs):
    project = Project.objects.filter(pk=1)[0:1].get()
    return render_to_response('search/indexes/project/project_text.txt', dict(object=project))



def thumbnail_get(project, fileobject, *args, **kwargs):
    
    ## Sets the default thumbnail to an image in the project.
    if not project.thumbnail:
        project.enf_consistancy()

    ## gets or creates thumbnail object
    try:
        thumbnail = thumbobject.objects.get_or_create(fileobject=project.thumbnail, filex = 128, filey = 128)[0]
    except:
        pass
    return thumbnail




def project_list_get(projects):

    listdata = []
    for project in projects:
        if project.enf_consistancy() == True:
            thumbnail = thumbnail_get(project=project, fileobject=project.thumbnail, filex = 128, filey = 128)
            listdata += [[project, thumbnail]]

    return listdata

'''
Printable Viewing

- Need to output an array of the printables thumbnails.
- Need to output the 3d render into a shadowbox via button click.
- Need to output the detailed information about the model (read me, files, additional text files, etc) into some kind of flexible format (to deal with java being disabled)
- Need to output comments
- Need to output statistics (tags, total # of downloads, total # of comments, total # of up votes, date uploaded into English formatted variables that change semantically to quantity (i.e., 1 download, 200 downloads/1 up vote, 200 up votes)
- Need to output download link for zip file for specific printable.
- Need to output author info (other work, 4 or 5) with thumbnail and name.
'''

def project(request, pk):
    project = Project.objects.filter(pk=pk).exclude(draft=True)[0:1].get()
    projectfiles = fileobject.objects.filter(project=project)
    mainthumb = thumbObjectProxy.objects.get_or_create(fileobject=project.thumbnail, filex = 250, filey = 250)[0]
    if project.enf_consistancy == False:
        raise Http404

    images=[]# Images in the project; will be handed to template
   # Get readme as first item in the list of texts to hand to the template.
    try:
        #Thus is in a try statement becouse the file backend might name the readme "ReadMe_1.md" or similar. Need to switch it out for "bodyfile" forighnkey at some point.
        readme = project.bodyFile
        htmlreadme=htmlobject.objects.get_or_create(fileobject = readme )[0]
        texts = [[htmlreadme, path.split(str(readme.filename))[1]]]
    except:
        texts = [[]]
        pass
   # norenders. this is the number of files in the project not rendered. We currently do nothing.. unless someone changed that and not this note.
    norenders =0
    print(project.get_adjusted_rating())
    for i in projectfiles:
        fullpath=i
        renderer=i.filetype

        if (renderer == "browser" or renderer == "jsc3d"):
            thumbmodel=thumbobject.objects.get_or_create(fileobject = i, filex=64, filey=64 )[0] 
            thumbnail=thumbmodel.filename.url
            images.append([thumbnail,fullpath,renderer])
        elif (renderer == "norender"):
            norenders +=1
        if (renderer == "text" and i != project.bodyFile ):
            htmlmodel=htmlobject.objects.get_or_create(fileobject = i )[0] 
            texts.append([htmlmodel, path.split(str(i.filename))[1]])
            

    download=zippedobject.objects.get_or_create(project=project)[0]

    c = RequestContext(request, dict(project=project, 
				user=request.user,
                                images=images, 
				texts=texts,
				galleryname="base", 
				mainthumb=mainthumb.filename.url,
                                downloadurl=download.filename.url))

    return render(request, "article.html", c)


def front(request):
 
    return render_to_response('list.html', dict(project=project, user=request.user,))

'''
- Needs to generate a list of the most popular printables of the day and/or week and/or month. The overhead of this is beyond me, but I imagine some sort of algorithm to factor in upvotes/downloads/comments and staff interest is needed to decide what is "popular".
'''
def list(request):
    """Main listing."""

###   get all the projects!   ###
    projects = Project.objects.exclude(draft=True).order_by("-created")

    paginator = Paginator(projects, 8)

    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        #only get thumbnails for projects on the current page.
        listdata = project_list_get(paginator.page(page))
    except (InvalidPage, EmptyPage):
        listdata = paginator.page(paginator.num_pages)
    return render_to_response("front.html", dict(listdata=listdata, user=request.user, active="home"))


from django.utils import simplejson

@csrf_exempt
@requires_csrf_token
def edit(request, pk):

##-----------------------------
# User filled and sent form
    try:
        project=Project.objects.filter(pk=pk)[0:1].get()
    except:
        return HttpResponse(status=404)
    if request.method == 'POST':
        form = ProjectForm(request.POST, project)
        #Check to make sure the form is valid and the user matches the project author
        if form.is_valid() and str(project.author) == str(request.user):
            #save thr form

          # Delete the old body text file... cause I'm a bad person and I don't know how to just open and write to the old one easily.
	    readme = project.bodyFile
            try:
                readme = project.bodyFile
                readmename = path.split(str(readme.filename))[1]
                readme.delete()
            except:
                pass
           # Save body as file
            bodyText = fileobject()
            bodyText.project = project


            from django.core.files.uploadedfile import UploadedFile
            import base64
            from io import BytesIO
            from io import TextIOWrapper
            from io import StringIO

           #io = TextIOWrapper(TextIOBase(form.cleaned_data["body"]))
            io = StringIO(form.cleaned_data["body"])
            txfl = UploadedFile(io)


            #editfield is renaming your readme to readme.md every time. That's not good.
            try:
                bodyText.filename.save(readmename, txfl)
            except:
                bodyText.filename.save('README.md', txfl)

            txfl.close()
            io.close()

            bodyText.save()
            project.bodyFile = bodyText
           #project.thumbnail = form.cleaned_data["thumbnail"]
            list_to_tags(form.cleaned_data["tags"], project.tags)
            project.save()
            return HttpResponseRedirect('/project/'+str(project.pk))
        else:
            if str(project.author) == str(request.user):
                return render_to_response('edit.html', dict(project=project, user=request.user, form=form, ))
            else:
                return HttpResponse(status=403)

#--------------------------
#Set up the actual view.


    elif str(project.author) == str(request.user):
        if project.bodyFile:
            readme = project.bodyFile.filename.read()
        else:
            readme = project.body

        taglist = []
        for i in project.tags.names():
           taglist.append(i)
        taglist = ",".join(taglist)

        thumbnailstring = "/"+path.split(project.thumbnail.filename.url)[1]
        form = ProjectForm({'body': readme, 'thumbnail': thumbnailstring, 'tags' : str(taglist)}, project)
        return render_to_response('edit.html', dict(project=project, user=request.user, form=form,))
        #return HttpResponse(response_data, mimetype="application/json")
    else:
        return HttpResponse(status=403)




@csrf_exempt
def create(request):
    try:
        project=Project.objects.filter(author=request.user).filter(draft=True)[0]
    except:
        project = Project()
        project.title = None
        project.draft=True
        project.author = request.user
        project.save()
##The form-----------------------------
    if request.method == 'POST':
        form = createForm(request.POST, project)
        form2 = defaulttag(request.POST)
        #Check to make sure the form is valid and the user matches the project author
        if form.is_valid() and form2.is_valid() and request.user.is_authenticated():
            #save thr form
            project.author = request.user
            project.title = form.cleaned_data["title"]


           # Save body as file
            bodyText = fileobject();
            bodyText.project = project


            from django.core.files.uploadedfile import UploadedFile
            import base64
            from io import BytesIO
            from io import TextIOWrapper
            from io import StringIO

           #io = TextIOWrapper(TextIOBase(form.cleaned_data["body"]))
            io = StringIO(form.cleaned_data["body"])
            txfl = UploadedFile(io)

            bodyText.filename.save('README.md', txfl)

            txfl.close()
            io.close()

            bodyText.save()


            project.author = request.user
           #project.thumbnail = form.cleaned_data["thumbnail"]
            project.draft=False
            project.save()
            list_to_tags(form.cleaned_data["tags"], project.tags)
            list_to_tags(form2.cleaned_data["categories"], project.tags, False)
            project.save()
            #add error if thumbnail is invalid
            return HttpResponseRedirect('/project/'+str(project.pk))
        else:
            return render_to_response('create.html', dict(user=request.user,  form=form, form2=form2,project=project))
#--------------------------
#Set up the actual view.
    elif request.user.is_authenticated():
        form = createForm("",project)
        form2 = defaulttag()

        return render_to_response('create.html', dict(user=request.user, form=form, form2=form2, project=project))
    else:
        return HttpResponse(status=403)

def tag(request,tag):
    projects = Project.objects.filter(tags__name__in=[tag]).order_by("-created")
    print("project.views.tag says projects are "+str(projects))
    paginator = Paginator(projects, 15)

    listdata = project_list_get(projects)

    print("listdata is "+str(listdata))
 
    paginator = Paginator(listdata, 8)

    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        listdata = paginator.page(page)
    except (InvalidPage, EmptyPage):
        listdata = paginator.page(paginator.num_pages)
    return render_to_response("front.html", dict(listdata=listdata, user=request.user, active="home"))



#   try: page = int(request.GET.get("page", '1'))
#   except ValueError: page = 1

#   try:
#       projects = paginator.page(page)
#   except (InvalidPage, EmptyPage):
#       projects = paginator.page(paginator.num_pages)

#   return render_to_response("list.html", dict(listdata=listdata, user=request.user))

def tagcloud(request):
    return render(request, "tagcloud.html")

def list_to_tags(list, tags, clear=True):
            if clear:
                tags.clear()
            for tag in list:
                tags.add(tag)


from djangoratings.views import AddRatingView
def ratingCalc(request, ):
    pass
#    response = HttpResponse(AddRatingFromModel()(request, **params))
    #response = HttpResponse("noresponese")
#    print(HttpResponse(AddRatingFromModel()(request, **params)))
#    print(response)

#    if response.status_code == 200:
#        if response.content == 'Vote recorded.':
#            print("successed the votething")
#        return {'message': response.content, 'score': params['score']}
#    return {'error': 9, 'message': response.content}

def thingtracker(request, pk):
    import os.path
    from django.utils import simplejson

    project = Project.objects.filter(pk=pk).exclude(draft=True)[0:1].get()
    projectfiles = fileobject.objects.filter(project=project)

    result=[{"type":"object"}]

    result.append({"properties":
			{"name":project.title,
			}
                  })

    
    things = []
    for i in projectfiles:
        things.append({"name":i.subfolder+os.path.split(str(i.filename.name))[1],
                       "size":i.filename.size,
                       "url":str(i.filename.url),
                       "delete_url":"/multi_delete/"+str(i.pk)+"/",
                       "delete_type":"POST",})
    result.append({"things":things})


    response_data = simplejson.dumps(result)

    #checking for json data type
    #big thanks to Guy Shapiro
    if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
        mimetype = 'application/json'
    else:
        mimetype = 'text/plain'
    return HttpResponse(response_data, mimetype=mimetype)



