from project.models import *
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from filemanager.models import fileobject
from project.models import Project
from django.conf import settings


###        This function validates the form for submitting projects. Excluding the title, thats only done in the createForm.
def cleanify(self, formName):

    cleaned_data = super(formName, self).clean()

   ###	make certain the selected thumbnail is valid	##
    try:
        thumb = cleaned_data["thumbnail"]
    except:
        thumb = ""

    files=fileobject.objects.filter(project=self.project)###	This gets a list of files from the project

    if thumb:
        noThumb = True
        for fl in files:
            if "uploads/"+str(self.project.pk)+thumb == str(fl.filename) and fl.filetype != "norender" and fl.filetype != "text":
                noThumb = False
                self.project.thumbnail = fl
                print("project.form settng "+self.project.title+"'s thumbnail to "+str(fl.filename))
                break
        if noThumb:
            self._errors['thumbnail'] = [u"The thumbnail you selected is not a valid uploaded image."]
    else:
        noThumb = True
        for fl in files:
            if fl.filetype != 'norender' and fl.filetype != "text":### Look for thumbnailable pic.
                noThumb = False
                self.project.thumbnail = fl
                print("project.form settng "+cleaned_data["title"]+"'s thumbnail to "+str(fl.filename))
                break
        if noThumb:
            self._errors['thumbnail'] = [u"None of your uploaded file makes a thumbnail!"]##	and an error if they all are.
    
   ###   make sure user wrote something about thier project.        
    if not cleaned_data['body']:
        self._errors['body'] = [u"Write something about your project! Jeezers."]
    print(self.project.enf_consistancy())
    if self.project.enf_consistancy() != True:
        self._errors['non_field_errors'] = [u"Something went wrong, and I have no idea what it was."]
    return cleaned_data



class ProjectForm(ModelForm):

    def __init__(self, request, project):
        self.project = project
        super(ProjectForm, self).__init__(request)

    class Meta:
        model = Project
        fields = ["tags"]

    body = forms.CharField(widget = forms.Textarea, required=False)
    thumbnail = forms.CharField(required=False)

    def clean(self):
        return cleanify(self, ProjectForm)


class createForm(ModelForm):

    def __init__(self, request, project):
        self.project = project
        if request:
            super(createForm, self).__init__(request)
        else:
            super(createForm, self).__init__()

    class Meta:
        model = Project
        fields = ["title", "tags",]

    def clean_title(self):
       data=self.cleaned_data["title"]
       if not data:
           raise forms.ValidationError("There is no title! You gotta have a title.") 
       return data

    body = forms.CharField(widget = forms.Textarea, required=False)
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
