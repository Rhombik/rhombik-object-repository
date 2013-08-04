from django import template
from django.conf import settings
from django.template import Context

register = template.Library()

@register.inclusion_tag('multiuploader/multiuploader_main.html', takes_context=True)
def multiupform(context):
    return context 
