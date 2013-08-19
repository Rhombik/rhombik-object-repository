from post.models import *
from django import forms
from django.forms import ModelForm


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["thumbnail", "body","tags",]

class createForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title","thumbnail", "body", "tags",]

class defaulttag(forms.Form):
    OPTIONS = (
    ("learning", "learning"),
    ("household", "househole"),
    ("abstract", "abstract"),
    ("game", "game")
    )
    categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         choices=OPTIONS)
