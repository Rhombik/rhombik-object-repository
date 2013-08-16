
from django.shortcuts import render
from django.template import RequestContext, loader

from post.models import Post
from django.contrib.auth.models import User
from userProfile.models import userProfile


def index(request, user):
    
    """bleh blebh bhel bleh, IM GOING INSANE.... I mean; user profile display stuff."""
    userdata=User.objects.filter(username=user).get()
    #help(Post.objects.filter)
    #print(user)
    userposts=Post.objects.all()#filter(author=user).get() '''~this needs to get the users posts.... not just you know, all the posts....'''
    #help(userposts)
    '''the correct answer was "print(userdata.get_profile().profilePicPath)"   '''
    c = RequestContext(request, dict(userPic=userdata.get_profile().profilePicPath, user=user, bio=userdata.get_profile().bio, userposts = userposts))
    return render(request, "userProfile/index.html", c)


