from django.contrib.auth.models import *

from django.forms import ModelForm
from captcha.fields import CaptchaField
from userProfile.models import *

class registerForm(ModelForm):
    class Meta:
        model = User
        fields = ["username","password"]
#    captcha = CaptchaField()

