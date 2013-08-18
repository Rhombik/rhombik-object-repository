from django.forms import ModelForm
from userProfile.models import *


class UserProfileForm(ModelForm):
    class Meta:
        model = userProfile
        fields = ["bio"]
