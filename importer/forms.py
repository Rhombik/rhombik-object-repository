
from django import forms

#It took me a long time to write a form with this kind of elegance and simplicity.
class ImportForm(forms.Form):
    url = forms.CharField(label='url')
