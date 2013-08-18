from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render

from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie

import thumbnailer.thumbnailer as thumbnailer 


from post.models import *
from post.forms import PostForm, createForm
from django import forms
##obviously ignoring csrf is a bad thing. Get this fixed.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse


def post(request, title,):

    """Single post with comments and a comment form."""
    c = RequestContext(request, dict(post=Post.objects.filter(title=title)[0:1].get(), user=request.user))
    return render(request, "article.html", c)

def list(request):
    """Main listing."""
    posts = Post.objects.all().order_by("-created")
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
        form = PostForm(request.POST)
        #Check to make sure the form is valid and the user matches the post author
        if form.is_valid() and str(post.author) == str(request.user):
            #save thr form
            post.body = form.cleaned_data["body"]
            post.thumbnail = form.cleaned_data["thumbnail"]
            post.tags = form.cleaned_data["tags"]
            post.save()
            return HttpResponseRedirect('/post/'+title)
        else:
            return HttpResponse(status=403)
#--------------------------
#Set up the actual view.


    elif str(post.author) == str(request.user):
        form = PostForm({'body': post.body, 'thumbnail': post.thumbnail, 'tags' : str(post.tags.distinct())})
        return render_to_response('edit.html', dict(post=post, user=request.user, form=form,))
        #return HttpResponse(response_data, mimetype="application/json")
    else:
        return HttpResponse(status=403)

@csrf_exempt
def create(request):

##The form-----------------------------
    if request.method == 'POST':
        form = createForm(request.POST)
        #Check to make sure the form is valid and the user matches the post author
        if form.is_valid() and request.user.is_authenticated():
            post = Post()
            #save thr form
            post.author = request.user
            post.title = form.cleaned_data["title"]
            post.body = form.cleaned_data["body"]
            post.author = request.user
            post.thumbnail = form.cleaned_data["thumbnail"]
            post.tags = form.cleaned_data["tags"]
            post.save()
            return HttpResponseRedirect('/post/'+form.cleaned_data["title"])
        else:
            return HttpResponse(status=403)
#--------------------------
#Set up the actual view.
    elif request.user.is_authenticated():
        form = createForm()
        return render_to_response('create.html', dict(user=request.user, form=form ))
    else:
        return HttpResponse(status=403)
