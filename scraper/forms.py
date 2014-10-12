
from django import forms

class ImportForm(forms.Form):
    url = forms.CharField(label='url')
