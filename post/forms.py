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

   ###	make certain the selected thumbnail is valid	##
    try:
        thumb = cleaned_data["thumbnail"]
    except:
        thumb = ""
    files=fileobject.objects.filter(post=self.post)###	This gets a list of files from the post

    if thumb:
        noThumb = True
        for fl in files:
            if "uploads/"+str(self.post.pk)+thumb == str(fl.filename):
                noThumb = False
                self.post.thumbnail = fl
                print(fl)
                break
        if noThumb:
            self._errors['thumbnail'] = [u"The thumbnail you selected is not an uploaded image."]
    else:
        noThumb = True
        for fl in files:
            if fl.filetype != 'norender':### Look for thumbnailable pic.
                noThumb = False
                self.post.thumbnail = fl
                break
        if noThumb:
            self._errors['thumbnail'] = [u"None of your uploaded file makes a thumbnail!"]##	and an error if they all are.
    
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
        fields = ["body","tags",]

    thumbnail = forms.CharField(required=False)

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
        fields = ["title", "body", "tags",]

    def clean_title(self):
       data=self.cleaned_data["title"]
       if not data:
           raise forms.ValidationError("There is no title! You gotta have a title.") 
       return data

    thumbnail = forms.CharField(required=False)

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
