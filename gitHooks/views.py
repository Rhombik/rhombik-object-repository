from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import urllib, urlparse
from django.conf import settings
from gitHooks.models import *
import json
@login_required
def register(request):
    account = githubAccount.objects.create(user=request.user)
    account.save()
    print(account.id)
    url='https://github.com/login/oauth/authorize/?'
    queryString={
        'client_id':settings.GIT_CLIENT_ID,
        'scope':"admin:repo_hook,write:repo_hook",
        'state':account.state,
                 }

    return(redirect(url + urllib.urlencode(queryString)))
#    return redirect("/")

def callback(request):
    account = githubAccount.objects.get(state=request.GET['state'])
    queryString={
        'client_id':settings.GIT_CLIENT_ID,
        'client_secret':settings.GIT_CLIENT_SECRET,
        'code':request.GET['code'],
    }
    accessToken = urllib.urlopen("https://github.com/login/oauth/access_token/?"+urllib.urlencode(queryString)).read()
    accessToken = urlparse.parse_qs(accessToken)
    account.scope=json.dumps(accessToken['scope'])
    account.access_token=accessToken['access_token'][0]
    account.token_type=accessToken['token_type'][0]
    account.save()
    return redirect("/mydrafts/")
