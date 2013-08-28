from django import forms
from django.forms import ModelForm
from userProfile.models import *

from django.contrib.auth.models import *
from captcha.fields import CaptchaField

class UserProfileForm(ModelForm):
    class Meta:
        model = userProfile
        fields = ["bio"]

class UserPictureForm(forms.Form):
        filename = forms.FileField(
            label='Select a file',
            help_text='max. 42 megabytes'
    )

class registerForm(ModelForm):
    class Meta:
        model = User
        fields = ["username","password"]
        
#    captcha = CaptchaField()###No no, it does work, but Its fucking annoying for testing.

