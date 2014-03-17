from django import template
from filemanager.models import fileobject 
from django.shortcuts import get_object_or_404, render_to_response
from django.template.loader import render_to_string

register = template.Library()

def raw_text(context):
    project=context['object']
    projectfiles = fileobject.objects.filter(project=project, filetype="text")
    textlist = "" 
    for i in projectfiles:
       textlist = textlist+i.filename.read()
    return textlist

register.simple_tag(takes_context=True)(raw_text)
