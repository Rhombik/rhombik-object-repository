from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth.models import User
from django.template import RequestContext, loader

from post.models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from userProfile.models import userProfile
from userProfile.forms import *


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


### This Is the view for the registration page.
@csrf_exempt
def register(request):
    
    ## If loop true when user clicks the register button.
    if request.method == 'POST':
        #get data from the forms
        form = registerForm(request.POST)
        profileform = UserProfileForm(request.POST)
        pictureform = UserPictureForm(request.POST, request.FILES)
        ## puts the users stuff in the database if its valid.
        if form.is_valid() and profileform.is_valid():# and pictureform.is_valid():
            ###Create the user
            data = User();
            data.username = form.cleaned_data["username"]
            #data.password = form.cleaned_data["password"]###this is NOT how you set a password! Passwords are hashed.
            data.set_password(form.cleaned_data["password"])
            data.save()
            ###Create user's profile
            profile = userProfile()
            profile.user = data
            profile.bio = profileform.cleaned_data["bio"]
            #Create users picture.
            try:
               profile.filename=request.FILES["filename"]
            except:
               profile.profilePicThumb=settings.URL+"/static/noUserPic.png"
               profile.profilePicPath=settings.URL+"/static/noUserPic.png"
               profile.profilePicType="browser"
               profile.filename="stoopid"
          # profile.filename.save(str(data.username)+"Pic-"+str(request.FILES["filename"]), request.FILES["filename"])
            print("profile.filename.path="+profile.filename.path)
            profile.save()
            return render_to_response('register.html', dict( user=request.user, msg="success. btw, don't click the submit button again."))
        #returns form with error messages.
        else:
            return render_to_response('register.html', dict( user=request.user, form=form, form2=profileform, form3=pictureform))
    
    ## Initializes the page with the forms.
    else:
        form = registerForm()
        profileform = UserProfileForm()
        pictureform = UserPictureForm()
        return render_to_response('register.html', dict( user=request.user, form=form, form2=profileform, form3=pictureform))

### simple logout view, redirects users to the login page.
def logout_user(request):
    logout(request)
    return redirect("/login")

### Login page.
@csrf_exempt
def login_user(request):
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        usernamedata = request.POST.get('username')
        passworddata = request.POST.get('password')
        user = authenticate(username=usernamedata, password=passworddata)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're success'd the log in!"
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    return render_to_response('auth.html',{'state':state, 'username': username})
