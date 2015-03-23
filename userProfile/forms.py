from django import forms
from django.forms import ModelForm
from userProfile.models import *

from django.contrib.auth.models import *
from captcha.fields import CaptchaField
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from crispy_forms.helper import FormHelper


class crispyLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(crispyLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

class crispyRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(crispyRegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)


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


