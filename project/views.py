from os import path

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render

from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie

import thumbnailer.thumbnailer as thumbnailer 


from filemanager.models import fileobject, thumbobject, htmlobject, zippedobject

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



def thumbnail_get(project, fileobject, *args, **kwargs):
    
    ## Sets the default thumbnail to an image in the project.
    if not project.thumbnail:
        Project.select_thumbnail(project)

    ## gets or creates thumbnail object
    thumbnail = thumbobject.objects.get_or_create(fileobject=project.thumbnail, filex = 128, filey = 128)[0]

    return thumbnail




def project_list_get(projects):

    listdata = []
    for project in projects:
        # if a project has no thumbnail. This happens when ignorant users delete thier pictures and navigate away without saving so they don't see the form error. #
########if not project.thumbnail:
########    print("I cant find the thumbnail for " + str(project))
########    # so we just get a new thumbnail for their project. #
########    Project.select_thumbnail(project)
        thumbnail = thumbnail_get(project=project, fileobject=project.thumbnail, filex = 128, filey = 128)
        listdata += [[project, thumbnail]]

    return listdata



def project(request, pk):
    project = Project.objects.filter(pk=pk).exclude(draft=True)[0:1].get()
    projectfiles = fileobject.objects.filter(project=project)
    mainthumb = thumbobject.objects.get_or_create(fileobject=project.thumbnail, filex = 250, filey = 250)[0]

    images=[]
    texts = []
    norenders =0

    for i in projectfiles:
        fullpath=i
        renderer=i.filetype

        if (renderer == "browser"):
            thumbmodel=thumbobject.objects.get_or_create(fileobject = i, filex=64, filey=64 )[0] 
            thumbnail=thumbmodel.filename.url
            images.append([thumbnail,fullpath,renderer])
        elif (renderer == "norender"):
            norenders +=1
        if (renderer == "text"):
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


def list(request):
    """Main listing."""

###   get all the projects!   ###
    projects = Project.objects.exclude(draft=True).order_by("-created")

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


from django.utils import simplejson

@csrf_exempt
@requires_csrf_token
def edit(request, pk):

##The form-----------------------------
    try:
        project=Project.objects.filter(pk=pk)[0:1].get()
    except:
        return HttpResponse(status=404)
    if request.method == 'POST':
        form = ProjectForm(request.POST, project)
        #Check to make sure the form is valid and the user matches the project author
        if form.is_valid() and str(project.author) == str(request.user):
            #save thr form
            project.body = form.cleaned_data["body"]
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
        taglist = []
        for i in project.tags.names():
           taglist.append(i)
        taglist = ",".join(taglist)
        print ("tags= "+str(taglist))
        thumbnailstring = "/"+path.split(project.thumbnail.filename.url)[1]
        form = ProjectForm({'body': project.body, 'thumbnail': thumbnailstring, 'tags' : str(taglist)}, project)
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
            project.body = form.cleaned_data["body"]
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
