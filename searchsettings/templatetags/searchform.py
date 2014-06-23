from django import template
from django.conf import settings
from django.template import Context
from searchsettings.forms import objectSearchForm

register = template.Library()

@register.inclusion_tag('search/searchform.html', takes_context=True)
def searchform(context):
    try:
        request = context['request']
        form = objectSearchForm(request.GET)
    except:
        "meh"
        form = objectSearchForm()

    return {'searchform': form}

