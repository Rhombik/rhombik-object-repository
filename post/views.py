from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render

from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie

import thumbnailer.thumbnailer as thumbnailer 

from post.models import *
from post.forms import PostForm, createForm, defaulttag
from django import forms
##obviously ignoring csrf is a bad thing. Get this fixed.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse


def post(request, title,):

    """Single post with comments and a comment form."""
    c = RequestContext(request, dict(post=Post.objects.filter(title=title).exclude(draft=True)[0:1].get(), user=request.user))
    return render(request, "article.html", c)

def list(request):
    """Main listing."""
    posts = Post.objects.exclude(draft=True).order_by("-created")
    paginator = Paginator(posts, 15)


    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    return render_to_response("list.html", dict(posts=posts, user=request.user))

from django.utils import simplejson

@csrf_exempt
def edit(request, title):

##The form-----------------------------
    try:
        post=Post.objects.filter(title=title)[0:1].get()
    except:
        return HttpResponse(status=404)
    if request.method == 'POST':
        form = PostForm(request.POST, post.pk)
        print("view's post.pk = "+str(post.pk))
        #Check to make sure the form is valid and the user matches the post author
        if form.is_valid() and str(post.author) == str(request.user):
            #save thr form
            post.body = form.cleaned_data["body"]
            post.thumbnail = form.cleaned_data["thumbnail"]
            list_to_tags(form.cleaned_data["tags"], post.tags)
            post.save()
            return HttpResponseRedirect('/post/'+title)
        else:
            if str(post.author) == str(request.user):
                return render_to_response('edit.html', dict(post=post, user=request.user, form=form,))
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
        form = PostForm({'body': post.body, 'thumbnail': post.thumbnail, 'tags' : str(taglist)}, post.pk)
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
        form = createForm(request.POST)
        form2 = defaulttag(request.POST)
        #Check to make sure the form is valid and the user matches the post author
        if form.is_valid() and form2.is_valid() and request.user.is_authenticated():
            #save thr form
            post.author = request.user
            post.title = form.cleaned_data["title"]
            post.body = form.cleaned_data["body"]
            post.author = request.user
            post.thumbnail = form.cleaned_data["thumbnail"]
            post.draft=False
            post.save()
            list_to_tags(form.cleaned_data["tags"], post.tags)
            list_to_tags(form2.cleaned_data["categories"], post.tags, False)
            post.save()
            #add error if thumbnail is invalid
            if post.thumbnailpath == "invalid":
                from django.forms.util import ErrorList
                errors = form._errors.setdefault("thumbnail", ErrorList())
                errors.append(u"No valid thumbnail file uploaded")
                return render_to_response('create.html', dict(user=request.user,  form=form, form2=form2,post=post))
            return HttpResponseRedirect('/post/'+form.cleaned_data["title"])
        else:
            return render_to_response('create.html', dict(user=request.user,  form=form, form2=form2,post=post))
#--------------------------
#Set up the actual view.
    elif request.user.is_authenticated():
        form = createForm()
        form2 = defaulttag()

        return render_to_response('create.html', dict(user=request.user, form=form, form2=form2,post=post))
    else:
        return HttpResponse(status=403)

def tag(request,tag):
    posts = Post.objects.filter(tags__name__in=[tag]).order_by("-created")
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
