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
    filename = None
#    filename = forms.ImageField(
#            label='Select a file',
#            help_text='This will be your profile pic',
#            required=False
#    )
#    pass        
class UserEmail(forms.Form):
    email = forms.EmailField(
            label='Email',
            help_text='(option, for password recovery)',
            required=False
    )
        

#class editForm(forms.Form):
#    password = forms.CharField(required=False)
    #class Meta:
    #    model = User
    #class Meta:
    #    model = User
    #    fields = ["password"]

class registerForm(ModelForm):
    class Meta:
        model = User
        fields = ["username","password"]
        
#    captcha = CaptchaField()###No no, it does work, but Its fucking annoying for testing.

