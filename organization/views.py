# Create your views here.
from django.shortcuts import render_to_response, render

from organization.models import *
from django import forms
from organization.forms import *
from django.http import HttpResponseRedirect, HttpResponse

def orgedit(request,organization):
    try:
        orgname=org.objects.filter(org_name=organization)[0:1]
    except:
        return HttpResponse(status=404)
    form = orgForm()

    return render_to_response('edit.html', dict(org=organization, form=form))


