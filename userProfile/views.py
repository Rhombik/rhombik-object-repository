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
from django.contrib.auth.forms import PasswordChangeForm





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
        print("redirecting")
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
            if pictureform.cleaned_data["filename"]:
                from avatarBot.models import uploadPic
                try:
                     upload = uploadPic.objects.filter( user = data )[0]
                     upload.delete()
                except: "whatever"
                upload = uploadPic.objects.create( user = data, filename = request.FILES["filename"] )
                upload.save()
                profile.avatarType = "upload"

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
    """THE VAMPIRE HEAD FIXES ALL OF YOUR BROKEN CODE!!!, that is to say, as long as you never look at this code, it could be anything. We guarantee that whatever you imaging is better written then what actually is written."""

    # userdata is the user data who's page we are viewing.
    userdata=User.objects.filter(pk = pk).get()

    posts=Post.objects.filter(author=userdata).order_by("-created") #'''~this needs to get the users posts.... not just you know, all the posts.... and now it does!''' YAY!

    #  paginator is neat!
    # It takes the list of posts and breaks them up into different pages.
    # Kinda obvious huh?
    paginator = Paginator(posts, 3*3)

    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    from avatarBot.avatarBot import getPic

    thumbpic, picfile, pictype = getPic(userdata, (256,256))

    c = RequestContext(request, dict(thumbpic = thumbpic, picfile = picfile, pictype = pictype, user=request.user, owner=userdata, posts = posts))
    return render(request, "userProfile/index.html", c)





### simple logout view, redirects users to the login page.
def logout_user(request):
    logout(request)
    return redirect("/register")





### This Is the view for the registration page.
@csrf_exempt
def register(request):
    
    from django.contrib.auth.forms import UserCreationForm

    ## If loop true when user clicks the register button.
    if request.method == 'POST':
        #get data from the forms
        form = UserCreationForm(request.POST)
        email = UserEmail(request.POST)
        if form.is_valid() and email.is_valid():
            ###Create the user
            data = User();
            data.username = form.cleaned_data["username"]
            if email.cleaned_data["email"]:
                data.email = email.cleaned_data["email"]
           #data.password = form.cleaned_data["password"]###this is NOT how you set a password! Passwords are hashed.
            data.set_password(form.cleaned_data["password1"])
            data.save()
            ###Create user's profile
            profile = userProfile()
            profile.user = data
         #  profile.bio = profileform.cleaned_data["bio"]
         #  #Create users picture.
         #  try:
         #      profile.filename=request.FILES["filename"]
         #  except: "null"
            profile.save()
         #  if profile.filename=="stoopid":
         #      return render_to_response('register.html', dict( user=request.user, msg="Your profile pic didn't work, unsupported or something. Don't worry though, you can use the cool default one I drew if you want. btw, don't click the submit button again."))
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
            login(request, user)
            return redirect("/editProfile/")
        #returns form with error messages.
        else:
            return render_to_response('register.html', dict( user=request.user, form=form, email=email))
    
    ## redirect to rlogin.
    else:
        return redirect("/rlogin/")




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
                ### right now logging in redirects you to home.
                ### it would be nice to have it redirect to where a user was going.
                ### like to the create page.
                return redirect("/")
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    else:
        return redirect("/rlogin/")

    from django.contrib.auth.forms import UserCreationForm
    form = UserCreationForm()
    email = UserEmail()
    return render_to_response('auth.html', {'form':form,'email':email, 'state':state, 'username': username})




### Register/login page.
@csrf_exempt ## <-- because alex is a terrible person
def rlogin(request):

    from django.contrib.auth.forms import UserCreationForm
    form = UserCreationForm()
    email = UserEmail()
    return render_to_response('rlogin.html', dict( user=request.user, form=form, email=email))



