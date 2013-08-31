from post.models import *
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError



class PostForm(ModelForm):

    def __init__(self, request, pk):
        self.pk = pk
        super(PostForm, self).__init__(request)

    class Meta:
        model = Post
        fields = ["thumbnail", "body","tags",]

    def clean(self):

        print("form says pk is "+str(self.pk))
        cleaned_data = super(PostForm, self).clean()

        ##make certain the selected thumbnail is valid
        import os
        if cleaned_data["thumbnail"] and not os.path.exists(settings.MEDIA_ROOT+"uploads/" + str(self.pk) + cleaned_data["thumbnail"]):
            raise ValidationError("The thumbnail you selected is not an uploaded image.")
        elif not os.path.splitext(cleaned_data["thumbnail"])[1] in [".stl",".obj",".STL",".OBJ", ".png",".jpg",".gif"]:
            raise ValidationError("The thumbnail you selected is not a valid image type.")
        return cleaned_data


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
