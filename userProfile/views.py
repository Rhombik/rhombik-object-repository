from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.shortcuts import render
from django.template import RequestContext, loader

from post.models import Post
from django.contrib.auth.models import User
from userProfile.models import userProfile
from django.views.decorators.csrf import csrf_exempt


#this obviously doesn't work... But it's a good base to work from.
@csrf_exempt
def edit(request):
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
            profile.filename = profileform.cleaned_data["filename"]
            profile.save
            return render_to_response('register.html', dict( user=request.user, msg="success"))
        else:
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
    """THE VAMPIRE HEAD FIXES ALL OF YOUR BROKEN CODE!!!, that is to say, as long as you never look at this code, it could be anything. We guarantee that whatever you imaging is better written then what actually is written."""
    userdata=User.objects.filter(username=user).get()
    
    posts=Post.objects.filter(author=userdata) #'''~this needs to get the users posts.... not just you know, all the posts.... and now it does!'''

    #posts = Post.objects.all().order_by("-created")
    paginator = Paginator(posts, 3*3)


    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    #help(userposts)
    '''the correct answer was "print(userdata.get_profile().profilePicPath)"   '''
    print(userdata.profile.profilePicType)
    c = RequestContext(request, dict(userPic=userdata.profile.profilePicPath, userPicThumb=userdata.profile.profilePicThumb, renderer=userdata.profile.profilePicType, usersname=user, bio=userdata.profile.bio, posts = posts))
    return render(request, "userProfile/index.html", c)


