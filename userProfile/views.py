
from django.shortcuts import render
from django.template import RequestContext, loader

from django.contrib.auth.models import User
from userProfile.models import userProfile


def index(request, user):

    """bleh blebh bhel bleh, IM GOING INSANE.... I mean; user profile display stuff."""
    userdata=User.objects.filter(username=user).get()
    help(userdata.userProfile.profilePicPath)
    c = RequestContext(request, dict(userPic=userdata.userProfile.profilePicPath, user=request.user, bio=userProfile.bio))
    return render(request, "article.html", c)


