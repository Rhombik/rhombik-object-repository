from post.models import *
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from filemanager.models import fileobject
from post.models import Post
from django.conf import settings


###        This function validates the form for submitting projects. Excluding the title, thats only done in the createForm.
def cleanify(self, formName):

    print("form says pk is "+str(self.post.pk))
    cleaned_data = super(formName, self).clean()

    ##make certain the selected thumbnail is valid
    import os
    thumb = fileobject.objects.filter(post = self.post, filename = "uploads/" + str(self.post.pk) + cleaned_data["thumbnail"])
    if cleaned_data["thumbnail"] and not thumb:
        raise ValidationError("The thumbnail you selected is not an uploaded image.")
    elif not cleaned_data["thumbnail"]:
        ##### this next bit is a wee hard to follow, so:
        files=fileobject.objects.filter(post=self.post)###	This gets a list of files from the post
        if all(['norender' == fltype for fltype in [fl.filetype for fl in files]]):###	This gets the .filetype value for all files and checks if they are all equal to 'norender'
            self._errors['thumbnail'] = [u"None of your uploaded file makes a thumbnail!"]##	and an error if they all are.
        else:
            for fl in files:
                if fl.filetype != 'norender':
                    cleaned_data["thumbnail"]="/"+os.path.split(str(fl.filename))[1]
                    break
    
    ###   make sure user wrote something about thier project.        
    if not cleaned_data['body']:
        self._errors['body'] = [u"Write something about your project! Jeezers."]

    return cleaned_data



class PostForm(ModelForm):

    def __init__(self, request, post):
        self.post = post
        super(PostForm, self).__init__(request)

    class Meta:
        model = Post
        fields = ["thumbnail", "body","tags",]

    def clean(self):
        return cleanify(self, PostForm)


class createForm(ModelForm):

    def __init__(self, request, post):
        self.post = post
        if request:
            super(createForm, self).__init__(request)
        else:
            super(createForm, self).__init__()

    class Meta:
        model = Post
        fields = ["title","thumbnail", "body", "tags",]

    def clean_title(self):
       data=self.cleaned_data["title"]
       if not data:
           raise forms.ValidationError("There is no title! You gotta have a title.") 
       return data

    def clean(self):
        return cleanify(self, createForm)


class defaulttag(forms.Form):
    OPTIONS = (
    ("learning", "learning"),
    ("household", "househole"),
    ("abstract", "abstract"),
    ("game", "game")
    )
    categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         choices=OPTIONS)
