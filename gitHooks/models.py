from django.db import models
import string
import random
from django.conf import settings
import urllib
from django.contrib.auth.models import User
from django.contrib import admin

def state_generator(size=20, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))

class githubAccount(models.Model):
    user = models.ForeignKey(User, related_name='user')
    scope = models.CharField(max_length=255 ,blank=True,)
    state = models.CharField(max_length=20 ,blank=True,)
    access_token = models.CharField(max_length=60 ,blank=True,)
    token_type = models.CharField(max_length=20 ,blank=True,)
    gitID = models.IntegerField(blank=True, null=True)
    gitUser = models.CharField(max_length=255 ,blank=True,)
    def save(self, *args, **kwargs):
        if not self.state:
            self.state=state_generator()
        super(githubAccount, self).save(*args, **kwargs)

    def get_access_token(self):
        url="https://github.com/login/oauth/access_token/?"
        queryString={
            'client_id':settings.GIT_CLIENT_ID,
            'code':self.code,
            'client_secret':settings.GIT_CLIENT_SECRET
                    }
                 
        urllib.urlopen(url + urllib.urlencode(queryString))
admin.site.register(githubAccount)
