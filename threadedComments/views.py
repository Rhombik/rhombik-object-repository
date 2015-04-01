
from threadedComments.models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.contenttypes.models import ContentType

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
##obviously ignoring csrf is a bad thing. Get this fixedo.
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
from threadedComments.forms import commentForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect,requires_csrf_token
from django.core.context_processors import csrf
from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponseForbidden

@csrf_exempt
def comment(request, content_type, content_pk, parent_id=None, comment_id=None):

    if not request.user:
        return HttpResponseForbidden

    object_type = ContentType.objects.get(model=content_type).model_class()
    if comment_id != "new":
        objectInstance = get_object_or_404(object_type, pk=comment_id)
    else:
        objectInstance = object_type(parent=parent_id)

    if objectInstance.pk and objectInstance.author != request.user:
        return HttpResponseForbidden

    if request.method == 'POST':
        form = commentForm(request.POST)
        if request.POST['action'] == "Submit":
            if not form.is_valid():
                return render(request, 'commentform.html', dict(form=form, content_pk=pk))
            form.save()
        if request.POST['action'] == "Delete":
            form.delete() 

        if request.POST['action'] == "Cancel":
            pass

        if "next" in request.GET and request.GET["next"]:
            return redirect(request.GET['next'])
        return redirect("/")

    else:
        form = commentForm(objectInstance)
        return render(request, 'commentform.html', dict(form=form, pk=content_pk))

