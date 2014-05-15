
from comments.models import *
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.contenttypes.models import ContentType
from comments.forms import commentForm

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
##obviously ignoring csrf is a bad thing. Get this fixedo.
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
from django.views.decorators.csrf import csrf_exempt, csrf_protect,requires_csrf_token
from django.core.context_processors import csrf


@csrf_exempt
def comment(request, content_type, pk, comment_id=-1):

    object_type = ContentType.objects.get(model=content_type)

## If the post doesn't exist 404 them
    try:
        objecty = object_type.get_object_for_this_type(pk=pk)
    except:
        return HttpResponse(status=404)

    print("objecty : "+str(objecty))

    if request.method == 'POST':
        form = commentForm(request.POST)
        if form.is_valid():
            #Save comment.
            commenttext = form.cleaned_data["commenttext"]
            parent=form.cleaned_data["parent"]
            comment = Comment(commenttext=commenttext, parent=parent,subject=objecty)
            comment.save()
   ########## I am so sorry. This redirect breaks the flexibility I was going for. This is very project.
            return HttpResponseRedirect('/project/'+str(objecty.pk))
        else:
            #Form errors
            print(" form is NOT valid")
            return render_to_response('commentform.html', dict(form=form, projectpk=pk))
    else:
        #Make a new form
        form = commentForm()
        form.fields['parent'].queryset = Comment.objects.filter(subject=objecty)
        return render_to_response('commentform.html', dict(form=form, projectpk=pk))


