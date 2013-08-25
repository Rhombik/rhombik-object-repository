from django import forms
from django.forms import ModelForm
from userProfile.models import *

class UserProfileForm(ModelForm):
    class Meta:
        model = userProfile
        fields = ["bio"]

class UserPictureForm(forms.Form):
        #model = userProfile
        #fields = ["bio"]
        filename = forms.FileField(
            label='Select a file',
            help_text='max. 42 megabytes'
    )
