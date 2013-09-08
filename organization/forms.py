from django.forms import ModelForm
from organization.models import *

class orgForm(ModelForm):
    class Meta:
        model = org

class cluster(ModelForm):
	class Meta:
		model = cluster
