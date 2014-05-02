from django import template
from django.conf import settings
from django.template import Context
from searchsettings.forms import DateRangeSearchForm

register = template.Library()

@register.inclusion_tag('search/searchform.html', takes_context=True)
def searchform(context):
    try:
        request = context['request']
        form = DateRangeSearchForm(request.GET)
    except:
        "meh"
        form = DateRangeSearchForm()

    return {'searchform': form}

