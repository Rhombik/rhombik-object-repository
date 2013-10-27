from os import path

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render

from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie

import thumbnailer.thumbnailer as thumbnailer 


from filemanager.models import fileobject, thumbobject, zippedobject

from post.models import Post
from post.forms import PostForm, createForm, defaulttag
from django import forms
##obviously ignoring csrf is a bad thing. Get this fixed.
from django.views.decorators.csrf import csrf_exempt, csrf_protect,requires_csrf_token
from django.core.context_processors import csrf

from django.http import HttpResponseRedirect, HttpResponse


def post(request, pk):
    print("pk is "+str(pk))
    post = Post.objects.filter(pk=pk).exclude(draft=True)[0:1].get()
    print("post is "+str(post))
    postfiles = fileobject.objects.filter(post=post)
    mainthumb = thumbobject.objects.get_or_create(fileobject=post.thumbnail, filex = 250, filey = 250)[0]
    images=[]
    for i in postfiles:
        fullpath=i.filename.url
        renderer=i.filetype
        thumbmodel=thumbobject.objects.get_or_create( fileobject = i, filex=64, filey=64 )[0] 
        thumbnail=thumbmodel.filename.url
        images.append([thumbnail,fullpath,renderer])

    download=zippedobject.objects.get_or_create(post=post)[0]
    print("^^ download url is "+str(download.filename.url))
    c = RequestContext(request, dict(post=post, 
				user=request.user,images=images, 
				galleryname="base", 
				mainthumb=mainthumb.filename.url,
                                downloadurl=download.filename.url))

    return render(request, "article.html", c)


def front(request):
 
    return render_to_response('list.html', dict(post=post, user=request.user,))


def list(request):
    """Main listing."""

###   get all the posts!   ###
    posts = Post.objects.exclude(draft=True).order_by("-created")

    listdata = []
    for post in posts:
        # if a post has no thumbnail. This happens when ignorant users delete thier pictures and navigate away without saving and seeing the form error. #
	if not post.thumbnail:
            print("I cant find the thumbnail for " + str(post))
            # so we just get a new thumbnail for their post. #
            Post.select_thumbnail(post)
        thumbnail = thumbobject.objects.get_or_create(fileobject=post.thumbnail, filex = 128, filey = 128)[0]
        listdata += [[post, thumbnail]]
    print("listdata is "+str(listdata))
 
    paginator = Paginator(listdata, 8)

    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        listdata = paginator.page(page)
    except (InvalidPage, EmptyPage):
        listdata = paginator.page(paginator.num_pages)
    print("listdata.object_list[?][0].title is "+str(listdata[0][0].title))
    print("listdata.object_list[?][1].filename is "+str(listdata[0][1].filename.url))
    return render_to_response("front.html", dict(listdata=listdata, user=request.user, active="home"))


from django.utils import simplejson

@csrf_exempt
@requires_csrf_token
def edit(request, pk):

##The form-----------------------------
    try:
        post=Post.objects.filter(pk=pk)[0:1].get()
    except:
        return HttpResponse(status=404)
    if request.method == 'POST':
        form = PostForm(request.POST, post)
        print("view's post.pk = "+str(post.pk))
        #Check to make sure the form is valid and the user matches the post author
        if form.is_valid() and str(post.author) == str(request.user):
            #save thr form
            post.body = form.cleaned_data["body"]
           #post.thumbnail = form.cleaned_data["thumbnail"]
            list_to_tags(form.cleaned_data["tags"], post.tags)
            post.save()
            return HttpResponseRedirect('/post/'+str(post.pk))
        else:
            if str(post.author) == str(request.user):
                return render_to_response('edit.html', dict(post=post, user=request.user, form=form, ))
            else:
                return HttpResponse(status=403)

#--------------------------
#Set up the actual view.


    elif str(post.author) == str(request.user):
        taglist = []
        for i in post.tags.names():
           taglist.append(i)
        taglist = ",".join(taglist)
        print ("tags= "+str(taglist))
        thumbnailstring = "/"+path.split(post.thumbnail.filename.url)[1]
        form = PostForm({'body': post.body, 'thumbnail': thumbnailstring, 'tags' : str(taglist)}, post)
        return render_to_response('edit.html', dict(post=post, user=request.user, form=form,))
        #return HttpResponse(response_data, mimetype="application/json")
    else:
        return HttpResponse(status=403)

@csrf_exempt
def create(request):
    try:
        post=Post.objects.filter(author=request.user).filter(draft=True)[0]
    except:
        post = Post()
        post.title = None
        post.draft=True
        post.author = request.user
        post.save()
##The form-----------------------------
    if request.method == 'POST':
        form = createForm(request.POST, post)
        form2 = defaulttag(request.POST)
        #Check to make sure the form is valid and the user matches the post author
        if form.is_valid() and form2.is_valid() and request.user.is_authenticated():
            #save thr form
            post.author = request.user
            post.title = form.cleaned_data["title"]
            post.body = form.cleaned_data["body"]
            post.author = request.user
           #post.thumbnail = form.cleaned_data["thumbnail"]
            post.draft=False
            post.save()
            list_to_tags(form.cleaned_data["tags"], post.tags)
            list_to_tags(form2.cleaned_data["categories"], post.tags, False)
            post.save()
            #add error if thumbnail is invalid
            return HttpResponseRedirect('/post/'+str(post.pk))
        else:
            return render_to_response('create.html', dict(user=request.user,  form=form, form2=form2,post=post))
#--------------------------
#Set up the actual view.
    elif request.user.is_authenticated():
        form = createForm("",post)
        form2 = defaulttag()

        return render_to_response('create.html', dict(user=request.user, form=form, form2=form2, post=post))
    else:
        return HttpResponse(status=403)

def tag(request,tag):
    posts = Post.objects.filter(tags__name__in=[tag]).order_by("-created")
    print("post.views.tag says posts are "+str(posts))
    paginator = Paginator(posts, 15)

    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    return render_to_response("list.html", dict(posts=posts, user=request.user))

def tagcloud(request):
    return render(request, "tagcloud.html")

def list_to_tags(list, tags, clear=True):
            if clear:
                tags.clear()
            for tag in list:
                tags.add(tag)
