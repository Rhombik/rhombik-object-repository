from project.models import *
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from filemanager.models import fileobject
from project.models import Project
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from taggit_autocomplete.widgets import TagAutocomplete


###        This function validates the form for submitting projects. Excluding the title, thats only done in the createForm.
def cleanify(self, formName):

    cleaned_data = super(formName, self).clean()

    print("the title is " + self.project.title)
    print("the preposed title is " + cleaned_data["title"])
    if self.project.title == cleaned_data["title"]:
        cleaned_data["title"]=""

   ###	make certain the selected thumbnail is valid	##
    try:
        thumb = cleaned_data["thumbnail"]
    except:
        thumb = ""
 
    parentType = ContentType.objects.get_for_model(self.project)
    files = fileobject.objects.filter(content_type__pk=parentType.id,object_id=self.project.id)###	This gets a list of files from the project

    if thumb:
        noThumb = True
        for fl in files:
            print(str(self.project.pk)+thumb)
            if "uploads/"+str(self.project.pk)+thumb == str(fl.filename) and fl.filetype != "norender" and fl.filetype != "text":
                noThumb = False
                self.project.thumbnail = fl
                break
        if noThumb:
            self._errors['thumbnail'] = [u"The thumbnail you selected is not a valid uploaded image."]
    else:

        if not self.project.enf_consistancy():
            self._errors['thumbnail'] = [u"None of your uploaded file makes a thumbnail!"]##	and an error if they all are.
    
   ###   make sure user wrote something about thier project.        
    if not cleaned_data['body']:
        self._errors['body'] = [u"Write something about your project! Jeezers."]
    if self.project.enf_consistancy() != True:
        self._errors['non_field_errors'] = [u"Something went wrong, and I have no idea what it was."]
    return cleaned_data



class ProjectForm(ModelForm):

    def __init__(self, request, project):
        self.project = project
        if request:
            super(ProjectForm, self).__init__(request)
        else:
            super(ProjectForm, self).__init__()

    class Meta:
        model = Project
        fields = ["title",]

    def clean_title(self):
       data=self.cleaned_data["title"]
       if not data:
           raise forms.ValidationError("There is no title! You gotta have a title.") 
       return data

    body = forms.CharField(widget = forms.Textarea, required=False)
    thumbnail = forms.CharField(required=False)
    tags = forms.CharField(widget=TagAutocomplete(attrs={'id': 'uploadTag'}),required=False)

    def clean(self):
        return cleanify(self, ProjectForm)


