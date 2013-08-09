from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render

from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie

import thumbnailer.thumbnailer as thumbnailer 


from post.models import *
from post.forms import PostForm
from django import forms
##obviously ignoring csrf is a bad thing. Get this fixed.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect


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

@csrf_exempt
def edit(request, title):
    post=Post.objects.filter(title=title)[0:1].get()
    if request.method == 'POST':
        form = PostForm(request.POST)
        #Check to make sure the form is valid and the user matches the post author
        if form.is_valid() and str(post.author) == str(request.user):
            #save thr form
            post.body = form.cleaned_data["body"]
            post.thumbnail = form.cleaned_data["thumbnail"]
            post.save()
            return HttpResponseRedirect('/post/'+title)
    elif str(post.author) == str(request.user):
        form = PostForm({'body': post.body, 'thumbnail': post.thumbnail})
        return render_to_response('edit.html', dict(post=post, user=request.user, form=form))
    else:
        return HttpResponse(status=403)


