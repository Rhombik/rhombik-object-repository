from post.models import *

from django.forms import ModelForm


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["thumbnail", "body",]

class createForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title","thumbnail", "body",]
