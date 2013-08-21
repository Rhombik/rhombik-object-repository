
from django.shortcuts import render
from django.template import RequestContext, loader

from post.models import Post
from django.contrib.auth.models import User
from userProfile.models import userProfile

#this obviously doesn't work... But it's a good base to work from.
#@csrf_exempt
def register(request):
    form = registerForm()
    if request.method == 'POST':
        form = registerForm(request.POST)
        profileform = UserProfileForm(request.POST)
        if form.is_valid() and profileform.is_valid():
            data = User();
            data.username = form.cleaned_data["username"]
            #data.password = form.cleaned_data["password"]
            data.set_password(form.cleaned_data["password"])
            data.save()
            profile = userProfile()
            profile.user = data
            profile.profilepic = "/"
            profile.bio = profileform.cleaned_data["bio"]
            profile.save
            return render_to_response('register.html', dict( user=request.user, msg="success"))
        else:
            print(request.POST)
            return render_to_response('register.html', dict( user=request.user, form=form, form2=profileform))#registerForm(request.POST)))#form, msg=form.errors))
    else:
        form = registerForm()
        profileform = UserProfileForm()
        return render_to_response('register.html', dict( user=request.user, form=form, form2=profileform))

def logout_user(request):
    logout(request)
    return redirect("/login")


def index(request, user):
    
    """bleh blebh bhel bleh, IM GOING INSANE.... I mean; user profile display stuff."""
    #I hate this vampire head ~alex
    userdata=User.objects.filter(username=user).get()
#<<<<<<< HEAD
#    c = RequestContext(request, dict(userPic=userdata.profile.profilePicPath, user=request.user, bio=userdata.profile.bio))
#    return render(request, "article.html", c)
    #help(Post.objects.filter)
    #print(user)
    userposts=Post.objects.filter(author=userdata) #'''~this needs to get the users posts.... not just you know, all the posts.... and now it does!'''
    #help(userposts)
    '''the correct answer was "print(userdata.get_profile().profilePicPath)"   '''
    c = RequestContext(request, dict(userPic=userdata.profile.profilePicPath, usersname=user, bio=userdata.profile.bio, posts = userposts))
    return render(request, "userProfile/index.html", c)


