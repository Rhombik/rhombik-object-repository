
from django.shortcuts import render
from django.template import RequestContext, loader

from post.models import Post
from django.contrib.auth.models import User
from userProfile.models import userProfile


def index(request, user):
    
    """bleh blebh bhel bleh, IM GOING INSANE.... I mean; user profile display stuff."""
    #I hate this vampire head ~alex
    userdata=User.objects.filter(username=user).get()
<<<<<<< HEAD
    c = RequestContext(request, dict(userPic=userdata.userProfile.profilePicPath, user=request.user, bio=userProfile.bio))
    return render(request, "article.html", c)
=======
    #help(Post.objects.filter)
    #print(user)
    userposts=Post.objects.filter(author=userdata) #'''~this needs to get the users posts.... not just you know, all the posts.... and now it does!'''
    #help(userposts)
    '''the correct answer was "print(userdata.get_profile().profilePicPath)"   '''
    c = RequestContext(request, dict(userPic=userdata.profile.profilePicPath, usersname=user, bio=userdata.profile.bio, userposts = userposts))
    return render(request, "userProfile/index.html", c)
>>>>>>> ad368b42bb83aa43cb949971e83ca73009b451a2


