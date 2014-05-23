
from comments.models import *
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

class commentForm(ModelForm):
   class Meta:
       model = Comment
       fields = ["commenttext", "parent"]
