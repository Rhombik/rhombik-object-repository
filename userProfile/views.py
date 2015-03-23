from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.contrib.auth.models import User
from django.template import RequestContext, loader

from project.models import Project
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from userProfile.models import userProfile
from django.contrib.auth.forms import PasswordChangeForm

from filemanager.models import fileobject

from project.views import project_list_get


##Delete the imports above this eventually
##Imports bellow this were added after alex's great rewrite, or confirmed as nessecarry.
from django.core.context_processors import csrf
from django.contrib import messages
from userProfile.forms import *
from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth import authenticate, login, logout

### This Is the view for the user edit page.
#it obviously ~~doesn't~~ Works... ~~But it's a good base to work from.~~
@csrf_exempt
def edit(request):
    
    # data is the users userdata.
    data = request.user

    ## redirect to login if not logged in.
    try:
        profile = userProfile.objects.filter(user=data)[0]
    except:
        return redirect("/register/")


    ##  User submitting profile data.
    if request.method == 'POST':

        #get data from the forms
        profileform = UserProfileForm(request.POST)
        pictureform = UserPictureForm(request.POST, request.FILES)

        ## puts the users stuff in the database if it is valid.
        if profileform.is_valid() and pictureform.is_valid():

            ###Create user's profile
            profile.bio = profileform.cleaned_data["bio"]

            #Create users picture.
            #if pictureform.cleaned_data["filename"]:
            if False:    
                  ## if they don't have a userpic yet we can't delete it.
                try:
                    profile.userpic.delete()
		except:
                    pass

                thumbiwumbi = fileobject(parent=profile)
                thumbiwumbi.filename = request.FILES["filename"]
                thumbiwumbi.save()
                profile.userpic = thumbiwumbi

            profile.save()
            return redirect("/userProfile/"+str(data.pk))

        #returns form with error messages.
        else:
            return render_to_response('editProfile.html', dict( user=request.user, form2=profileform, form3=pictureform))


    ## Initializes the page with the forms.
    else:
        #form = PasswordChangeForm(data)
        profileform = UserProfileForm({'bio':profile.bio})
        pictureform = UserPictureForm()#{"filename":profile.})
        return render_to_response('editProfile.html', dict( user=request.user, form2=profileform, form3=pictureform))

def index(request, pk):
    
    """bleh blebh bhel bleh, IM GOING INSANE.... I mean; user profile display stuff."""
    #I hate this vampire head ~alex
    """THE VAMPIRE HEAD FIXES ALL OF YOUR BROKEN CODE!!!, that is to say, as long as you never look at this code, it could be anything. We guarantee that whatever you imaging is better written then what actually is written*."""
    """*because what you are imagining has not yet been forced through the harsh filter of clarification"""


    # userdata is the user data who's page we are viewing.
    userdata=User.objects.filter(pk = pk).get()

    profile = userProfile.objects.filter(user=userdata)[0]

    projects=Project.objects.filter(author=userdata).exclude(draft=True).order_by("-created") #'''~this needs to get the users projects.... not just you know, all the projects.... and now it does!''' YAY!  And now it gets no projects? wtf.. ok, so it is getting the list.. it is just not getting displayed...

    #  paginator is neat!
    # It takes the list of projects and breaks them up into different pages.
    # Kinda obvious huh?
    paginator = Paginator(projects, 3*3)

    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        projects = paginator.page(page)
    except (InvalidPage, EmptyPage):
        projects = paginator.page(paginator.num_pages)

    listdata = project_list_get(projects)

    try:
        thumbpic = [profile.userpic.get_thumb(512,512)]
    except:
        thumbpic = False

    c = {"thumbpic":thumbpic, 
        "user":request.user,
        "owner":userdata,
        "listdata":listdata
        }

    return render(request, "userProfile/index.html", c)

def logoutView(request):
    logout(request)
    if "next" in request.POST and request.POST["next"]:
        return redirect(request.POST['next'])
    return redirect("/")



def legister(request):
    if request.method == 'POST':
        user=None
        loggedin=False 
        if request.POST['action'] == 'Register':
            loginForm = crispyLoginForm()
            registerForm = crispyRegisterForm(request.POST)
            if registerForm.is_valid():
                user = User.objects.create_user(request.POST['username'],"",  password=request.POST['password1'])
                user = authenticate(username=request.POST['username'], password=request.POST['password1'])

        if request.POST['action'] == 'Login':
            loginForm = crispyLoginForm(data=request.POST)
            registerForm = crispyRegisterForm()
            if loginForm.is_valid():
                user = authenticate(username=request.POST['username'], password=request.POST['password'])
        else:#This should never get called, but it was breaking when I submitted the wrong data, and I did this to test, and it makes it fail gracefully.
            loginForm = crispyLoginForm()
            registerForm = crispyRegisterForm()

        ##Logs the user in.
        if user is not None:
            if user.is_active:
                login(request, user)
                loggedin=True

        c = {
            "loginForm":loginForm,
            "registerForm":registerForm
        }

        c.update(csrf(request))

        if (loggedin or registerForm.is_valid()) and "next" in request.POST and request.POST["next"]:
            return redirect(request.POST['next'])
        elif loggedin or registerForm.is_valid():
            return redirect("/")

        return render(request, "legister.html", c)



    if request.method == 'GET':
        loginForm = crispyLoginForm()
        registerForm = crispyRegisterForm()
        c = {
            "loginForm":loginForm,
            "registerForm":registerForm,
            "next":getattr(request.GET, 'next', "")
        }
        c.update(csrf(request))
        return render(request, "legister.html", c)
