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
        #post=Post.objects.filter(title=)[0:1].get()

        ##make certain the selected thumbnail is valid, and generate
        if cleaned_data["thumbnail"]:
            try:
                import thumbnailer.thumbnailer
                ##I hate names.
                thumbnail = thumbnailer.thumbnailer.thumbnail(settings.MEDIA_ROOT+"uploads/" + str(self.pk) + cleaned_data["thumbnail"],(128,128))
                #thumbnail[2] != "norender"
                #cleaned_data["thumbnail"] = str(thumbnail[0])
            except:
                clened_data["thumbnail"] = "invalid"
                #from django.core.exceptions import ValidationError
                #raise ValidationError('No valid thumbnail')
        else:
            ##If no thumbnail is selected, pick one randomly and generate a thumb
            import filemanager.models
            postfiles = filemanager.models.fileobject.objects.filter(post=self.pk).exclude(filetype="norender")[0]
            cleaned_data["thumbnail"]=str(postfiles.filename)#thumbnail=thumbnailpath = thumbnailer.thumbnailer.thumbnail(postfiles.filename.path,(128,128))[0]
        #super().clean(self) 
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
