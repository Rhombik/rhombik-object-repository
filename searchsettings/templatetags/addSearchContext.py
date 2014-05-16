from django import template
from filemanager.models import fileobject 
from django.shortcuts import get_object_or_404, render_to_response
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType

register = template.Library()

def raw_text(context):
    project=context['object']
    object_type = ContentType.objects.get_for_model(project)
    projectfiles = fileobject.objects.filter(content_type=object_type,object_id=project.id, filetype="text")


    textlist = "" 
    for i in projectfiles:
       textlist = textlist+i.filename.read()
    return textlist

register.simple_tag(takes_context=True)(raw_text)

