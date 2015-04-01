
from threadedComments.models import *
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Button, HTML, Div, Field


class commentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(commentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

    commenttext = forms.CharField(widget = forms.Textarea, required=True, label='Comment')

    class Meta:
        model = Comment
        fields = ["commenttext", "parent"]
