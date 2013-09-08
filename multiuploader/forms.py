from django import forms

class MultiuploaderImage(forms.Form):
    """Model for storing uploaded photos"""
    image = forms.FileField()

