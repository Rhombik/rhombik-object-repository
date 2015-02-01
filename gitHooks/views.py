from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import urllib
from django.conf import settings
from gitHooks.models import *

@login_required
def register(request):
    account = githubAccount.objects.create(user=request.user)
    account.save()
    print(account.id)
    url='https://github.com/login/oauth/authorize/?'
    queryString={
        'client_id':settings.GIT_CLIENT_ID,
        'scope':"",
        'state':account.state,
                 }

    print(url + urllib.urlencode(queryString))
    return
#    return redirect("/")

def callback(request):
    print(request.GET['state'])
    account = githubAccount.objects.get(state=request.GET['state'])
    print(account)
    account.code = request.GET['code']
    account.scope = request.GET['scope']
    account.save()
    return redirect("/mydrafts/")
