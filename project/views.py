from os import path

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse

from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie

import thumbnailer.thumbnailer as thumbnailer 


from filemanager.models import fileobject, thumbobject, htmlobject, zippedobject 

from project.models import Project
from project.forms import ProjectForm
from django import forms

from django.contrib.contenttypes.models import ContentType
from django.http import Http404


"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
##obviously ignoring csrf is a bad thing. Get this fixedo.
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
from django.views.decorators.csrf import csrf_exempt, csrf_protect,requires_csrf_token
from django.core.context_processors import csrf

def searchtest(*args, **kwargs):
    project = Project.objects.filter(pk=1).get()
    return render_to_response('search/indexes/project/project_text.txt', dict(object=project))

from django.shortcuts import redirect
def delete(RequestContext, pk):
    request=RequestContext
    project = Project.objects.get(pk=pk)
    response_data = False
    if str(project.author) == str(request.user):
        project.delete()
        response_data = True

    if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
        mimetype = 'application/json'
        return HttpResponse(response_data, mimetype=mimetype)
    return redirect("/mydrafts/")

## this function is for the mydrafts page to publish things. It relies on the project.valid bool, which should be set within editOrCreateStuff.
def publish(request, pk):
    project = Project.objects.get(pk=pk)
    response_data = False
    if str(project.author) == str(request.user) and project.valid == True:
        project.draft = False
        project.save()
        response_data = True

    if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
        mimetype = 'application/json'
        return HttpResponse(response_data, mimetype=mimetype)
    return redirect("/mydrafts/")

"""______________________________"""
## project_list_get takes a list of projects and returns a list of lists containing:
## -a thumbnail object for the project.
## -the project.
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
def project_list_get(projects, purge=True):

    listdata = []
    for project in projects:
        if project.enf_consistancy() == True or purge == False:
            object_type = ContentType.objects.get_for_model(project)
            try: 
                project.thumbnail
                thumbnail = project.thumbnail.get_thumb(300,200)
            except:
                thumbnail = [""]
            listdata += [[project, thumbnail[0]]]

    return listdata




def project(request, pk):

## Try to get the project from the database. If this fails than return 404.
    try:
        project = Project.objects.exclude(draft=True).get(pk=pk)
    except:
        raise Http404


    object_type = ContentType.objects.get_for_model(project)
    projectfiles = fileobject.objects.filter(content_type=object_type,object_id=project.id)


    if project.enf_consistancy == False:
        raise Http404
    else:
        mainthumb = project.thumbnail.get_thumb(650,500)

    images=[]# Images in the project; will be handed to template

   # Get readme as first item in the list of texts to hand to the template.
    try:
        #Thus is in a try statement becouse the file backend might name the readme "ReadMe_1.md" or similar. Need to switch it out for "bodyfile" forighnkey at some point.
        readme = project.bodyFile
        htmlreadme=htmlobject.objects.get_or_create(fileobject = readme )[0]
        texts = [[htmlreadme, path.split(str(readme.filename))[1]]]
    except:
        texts = []
        pass
   # norenders. this is the number of files in the project not rendered. We currently do nothing.. unless someone changed that and not this note.
    norenders =0
    for i in projectfiles:
        thumb=i.get_thumb(65,50)
        renderer=i.filetype
        if renderer != "norender" and renderer != "text":
            images.append(thumb)
        if renderer == "norender":
            norenders +=1
        if renderer == "text" and i != project.bodyFile :
            htmlmodel=htmlobject.objects.get_or_create(fileobject = i )[0] 
            texts.append([htmlmodel, path.split(str(i.filename))[1]])
    download=zippedobject.objects.get_or_create(project=project)[0]
    author = project.author
    from userProfile.models import userProfile
    authorprofile = userProfile.objects.filter(user=author)[0]
    try:
        authorpic=authorprofile.userpic.get_thumb(128,128)[0]
    except:
        authorpic=False

    ## get the root comment of the project and use it to get all the projects comments.
    from comments.models import CommentRoot
    object_type = ContentType.objects.get(model="project")
    commentRoot = CommentRoot.objects.get_or_create(commenter=project.author, content_type=object_type, object_id=project.pk)[0]
    nodes = commentRoot.get_descendants(include_self=False)
    ## Put the comments in the comment form. Then users can only use this form to reply to comments on this project.
    from comments.forms import commentForm
    commentform = commentForm()
    commentform.fields['parent'].queryset = nodes
    if download.filename:
        downloadurl=download.filename.url
    else:
        downloadurl=None

    c = RequestContext(request, dict(project=project, 
				user=request.user,

				author=author,
				authorprofile=authorprofile,
				authorpic=authorpic,

                                commentRootId=commentRoot.id,
                                nodes=nodes,
				commentform=commentform,
                                moreobjects=norenders,
                                images=images, 
				texts=texts,
				galleryname="base", 
				mainthumb=[mainthumb],
                                downloadurl=downloadurl))
    return render(request, "article.html", c)


def front(request):
 
    return render_to_response('list.html', dict(project=project, user=request.user,))



'''
- Needs to generate a list of the most popular printables of the day and/or week and/or month. The overhead of this is beyond me, but I imagine some sort of algorithm to factor in upvotes/downloads/comments and staff interest is needed to decide what is "popular".
'''
def list(request):
    """Main listing."""

###   get all the projects!   ###
    newprojects = Project.objects.exclude(draft=True).order_by("-created")

    paginator = Paginator(newprojects, 8)

    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        #only get thumbnails for projects on the current page.
        listdata = project_list_get(paginator.page(page))
    except (InvalidPage, EmptyPage):
        listdata = paginator.page(paginator.num_pages)
    return render_to_response("front.html", dict(listdata=listdata, projectcount=newprojects.count(), user=request.user, active="home"))


from django.utils import simplejson



'''
 Here lives stuff for the edit and create a project pages.
'''

def editOrCreateStuff(project, request):

  if request.user.is_authenticated() and str(project.author) == str(request.user):


    project.valid=False
    project.save()


  ## postmode! We are getting pretty post data from the user!!!

    if request.method == 'POST':

        if(request.POST['action']=="Delete"):
            project.delete()
            return HttpResponseRedirect('/mydrafts/')

    ## get the forms and check that they are valid

        form = ProjectForm(request.POST.copy(), project)
        if form.is_valid():
            project.valid=True

    ## Title related stuff. Setting it, making sure it's still there, whatever.

        if "title" in form.cleaned_data and form.cleaned_data["title"]: # if that data is not a blank string
            project.title = form.cleaned_data["title"] # than we do change the title
        else:
            form.data['title'] = project.title

      # Editing the Readme.md file stuff.
        project.saveReadme(form.cleaned_data["body"])
     # Done with editing the README.md textfile.

        list_to_tags(form.cleaned_data["tags"], project.tags)

   #### All this fun stuff is handeling what happens for trying to publish vs trying to save the project.
        if project.valid:
            if(request.POST['action']=="Publish"):
                project.draft=False
                project.save()
                return HttpResponseRedirect('/project/'+str(project.pk))
            elif(request.POST['action']=="Save"):
                project.save()
                return HttpResponseRedirect('/mydrafts/')
        else:
            project.save()
            draftSaved = True
            return render_to_response('edit.html', dict(project=project, user=request.user, form=form, draftSaved=draftSaved, ))

   #### Not POSTmode! We are setting up the form for the user to fill in. We are not getting form data from the user.

    else:

	form = project.get_form()## this gets a form filled with the projects data
        form.errors['title'] = ""#form['body'].error_class()
        form.errors['thumbnail'] = ""#form['body'].error_class()
        form.errors['body'] = ""#form['body'].error_class()
        return render_to_response('edit.html', dict(project=project, user=request.user, form=form,))

  else:
      return HttpResponse(status=403)


@csrf_exempt
@requires_csrf_token
def edit(request, pk):

## Get the project the user wishes to edit.
    project=Project.objects.filter(pk=pk)[0]

    return editOrCreateStuff(project, request)


@csrf_exempt
def create(request):
    if Project.objects.filter(author=request.user).filter(draft=True).count() >= 12:#cause it's funny
        project=Project.objects.filter(author=request.user).filter(draft=True)[0]
    else:
        project = Project()
        project.title = None
        project.draft=True
        project.author = request.user
        project.save()

    return editOrCreateStuff(project, request)


## This view is moribund. It may be reserected or exercised at some point.
def tag(request,tag):
    projects = Project.objects.filter(tags__name__in=[tag]).order_by("-created")
    paginator = Paginator(projects, 15)

    listdata = project_list_get(projects)

 
    paginator = Paginator(listdata, 8)

    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        listdata = paginator.page(page)
    except (InvalidPage, EmptyPage):
        listdata = paginator.page(paginator.num_pages)
    return render_to_response("front.html", dict(listdata=listdata, user=request.user, active="home"))


def tagcloud(request):
    return render(request, "tagcloud.html")


## I take a csv and add it to a taggit manager.
def list_to_tags(data, tags, clear=True):
            data=data.split(',')
            if clear:
                tags.clear()
            for tag in data:
                tags.add(tag)


from djangoratings.views import AddRatingFromModel
def ratingCalc(request,**params):
    response = AddRatingFromModel()(request, **params)
    project= Project.objects.get(pk=params['object_id'])
    if response.status_code == 200:
        project.calc_adjusted_rating()
        pass
    return response




def thingtracker(request, pk):
    import os.path
    import json

    project = Project.objects.filter(pk=pk).exclude(draft=True)[0:1].get()
    projectfiles = fileobject.objects.filter(project=project)

    result=[{"type":"object"}]

    result.append({"properties":
			{"name":project.title,
			}
                  })

    
    things = []
    for i in projectfiles:
        things.append({"title":i.subfolder+os.path.split(str(i.filename.name))[1],
                       "size":i.filename.size,
                       "url":str(i.filename.url),
                       })
    result.append({"things":things})


    response_data = json.dumps(result,sort_keys=True,
                  indent=4, separators=(',', ': '))

    #checking for json data type
    #big thanks to Guy Shapiro
    if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
        mimetype = 'application/json'
    else:
        mimetype = 'text/plain'
    return HttpResponse(response_data, mimetype=mimetype)



