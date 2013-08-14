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

