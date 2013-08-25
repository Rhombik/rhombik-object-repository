# Create your views here.
from basiclogin.forms import *
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from userProfile.forms import *

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect

from filemanager.models import filename

@csrf_exempt
def register(request):
    form = registerForm()
    if request.method == 'POST':
        form = registerForm(request.POST)
        profileform = UserProfileForm(request.POST)
        pictureform = UserPictureForm(request.POST, request.FILES)
        if form.is_valid() and profileform.is_valid():
            #Creat the user
            data = User();
            data.username = form.cleaned_data["username"]
            #data.password = form.cleaned_data["password"]###this is NOT how you set a password!
            data.set_password(form.cleaned_data["password"])
            data.save()
            #Create users profile
            profile = userProfile()
            profile.user = data
            profile.save()
           #profile.profilepic = "/"
            profile.bio = profileform.cleaned_data["bio"]
            newuserpic = filename(filename = request.FILES["filename"])##take a letter...
            newuserpic.save()
            profile.profilePicPath = newuserpic.thumbnailpath
            print("thumbnailpath:"+profile.profilePicPath)
            #profile.filename.filename.save
            #profile.filename = newuserpic
            profile.save()
           #print(profile.filename.filename.path)
            return render_to_response('register.html', dict( user=request.user, msg="success. btw, don't click the submit button again."))
        else:
            print(request.FILES)
            return render_to_response('register.html', dict( user=request.user, form=form, form2=profileform, form3=pictureform))#registerForm(request.POST)))#form, msg=form.errors))
    else:
        form = registerForm()
        profileform = UserProfileForm()
        pictureform = UserPictureForm()
        return render_to_response('register.html', dict( user=request.user, form=form, form2=profileform, form3=pictureform))

def logout_user(request):
    logout(request)
    return redirect("/login")

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
