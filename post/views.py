from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render

from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie

import thumbnailer.thumbnailer as thumbnailer 


from post.models import *
from multiuploader.models import *


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

def edit(request, title,):
    items = MultiuploaderImage.objects.all()
    post=Post.objects.filter(title=title)[0:1].get()
    return render_to_response('edit.html', dict(items=items, posts=post, user=request.user))


