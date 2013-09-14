from django import forms
from django.forms import ModelForm
from userProfile.models import *

#from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import *
from captcha.fields import CaptchaField

# 1 from post.models import *
# 2 from django import forms
# 3 from django.forms import ModelForm
# 4 from django.core.exceptions import ValidationError
# 5 from filemanager.models import fileobject
# 6 from post.models import Post
# 7 from django.conf import settings
# 8 
# 9 
#10 ###        This function validates the form for submitting projects. Excluding the title, thats only done in the createForm.
#11 def cleanify(self, formName):
#12 
#13     print("form says pk is "+str(self.post.pk))
#14     cleaned_data = super(formName, self).clean()
#15 
#16     ##make certain the selected thumbnail is valid
#17     import os
#18     thumb = fileobject.objects.filter(post = self.post, filename = "uploads/" + str(self.post.pk) + cleaned_data["thumbnail"])
#19     if cleaned_data["thumbnail"] and not thumb:
#20         raise ValidationError("The thumbnail you selected is not an uploaded image.")
#21     elif not cleaned_data["thumbnail"]:
#22         ##### this next bit is a wee hard to follow, so:
#23         files=fileobject.objects.filter(post=self.post)###      This gets a list of files from the post
#24         if all(['norender' == fltype for fltype in [fl.filetype for fl in files]]):###  This gets the .filetype value for all files     and checks if they are all equal to 'norender'
#25             self._errors['thumbnail'] = [u"None of your uploaded file makes a thumbnail!"]##    and an error if they all are.
#26         else:
#27             for fl in files:
#28                 if fl.filetype != 'norender':
#29                     cleaned_data["thumbnail"]="/"+os.path.split(str(fl.filename))[1]
#30                     break
#31 
#32     ###   make sure user wrote something about thier project.        
#33     if not cleaned_data['body']:
#34         self._errors['body'] = [u"Write something about your project! Jeezers."]
#35 
#36     return cleaned_data


class UserProfileForm(ModelForm):
    class Meta:
        model = userProfile
        fields = ["bio"]

class UserPictureForm(forms.Form):
    filename = forms.FileField(
            label='Select a file',
            help_text='This will be your profile pic',
            required=False
    )
        
class UserEmail(forms.Form):
    email = forms.EmailField(
            label='Email',
            help_text='(option, for password recovery)',
            required=False
    )
        

#class editForm(forms.Form):
#    password = forms.CharField(required=False)
    #class Meta:
    #    model = User
    #class Meta:
    #    model = User
    #    fields = ["password"]

class registerForm(ModelForm):
    class Meta:
        model = User
        fields = ["username","password"]
        
#    captcha = CaptchaField()###No no, it does work, but Its fucking annoying for testing.

