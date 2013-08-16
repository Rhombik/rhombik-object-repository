# Create your views here.
from basiclogin.forms import *
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect, csrf_exempt

@csrf_exempt
def register(request):
    form = registerForm()
    if request.method == 'POST':
        form = registerForm(request.POST)
        if form.is_valid():
            data = User();
            data.username = form.cleaned_data["username"]
            data.password = form.cleaned_data["password"]
            data.save()
            return render_to_response('register.html', dict( user=request.user, msg="success"))
        else:
            return render_to_response('register.html', dict( user=request.user, msg="Form is invalid"))
    else:
        form = registerForm()
        return render_to_response('register.html', dict( user=request.user, form=form,))


def login_user(request):
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    return render_to_response('auth.html',{'state':state, 'username': username})