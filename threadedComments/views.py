
from threadedComments.models import *
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.contenttypes.models import ContentType
from threadedComments.forms import commentForm

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


    if request.method == 'POST':
        form = commentForm(request.POST)
        if(request.POST['action']=="Cancel"):
            return HttpResponseRedirect('/project/'+str(objecty.pk))
        elif form.is_valid():
            #Save comment.
            commenttext = form.cleaned_data["commenttext"]
            ## If the comment is replying to another comment, thats fine, otherwise we set the parent to the root comment.
            if(form.cleaned_data["parent"]):
                parent=form.cleaned_data["parent"]
            else:
                parent = CommentRoot.objects.get(content_type=object_type, object_id=objecty.pk)

            commenter=request.user
            comment = Comment(
			commenttext=commenttext,
			commenter=commenter,
			parent=parent
			)
            comment.save()
   ########## I am so sorry. This redirect breaks the flexibility I was going for. This is very project.
            return HttpResponseRedirect('/project/'+str(objecty.pk)+"#comment="+str(comment.pk))
        else:
            #Form errors
            return render_to_response('commentform.html', dict(form=form, projectpk=pk))
    else:
        #Make a new form
        form = commentForm()
        if comment_id==-1:
            form.fields['parent'].queryset = CommentRoot.objects.get(content_type=object_type, object_id=objecty.pk).get_descendants(include_self=False)
        else:
            from django import forms
            form.fields['parent'].widget = forms.HiddenInput()
            form.fields['parent'].initial = Comment.objects.get(pk=comment_id)
        return render_to_response('commentform.html', dict(form=form, projectpk=pk))


@csrf_protect
def editComment(request, content_type, pk, comment_id=-1):

    object_type = ContentType.objects.get(model=content_type)

## If the post doesn't exist 404 them
    try:
        objecty = object_type.get_object_for_this_type(pk=pk)
    except:
        return HttpResponse(status=404)

    editingComment = Comment.objects.get(pk=comment_id)
    if not (request.user.is_authenticated() and str(editingComment.commenter) == str(request.user)):
        return HttpResponse(status=404)
    elif request.method == 'POST':
        form = commentForm(request.POST)
        if(request.POST['action']=="Delete"):
            parent_pk=editingComment.parent
            editingComment.delete()
            return HttpResponseRedirect('/project/'+str(objecty.pk)+"#comment="+str(parent_pk))
        elif(request.POST['action']=="Cancel"):
            return HttpResponseRedirect('/project/'+str(objecty.pk)+"#comment="+str(editingComment.parent.pk))
        elif form.is_valid():
            editingComment.commenttext=form.cleaned_data["commenttext"]
            editingComment.save()
   ########## I am so sorry. This redirect breaks the flexibility I was going for. This is very project.
   #### ( this is in reference to the general objecty get_object_for_this_type thing I had going ) ####
            return HttpResponseRedirect('/project/'+str(objecty.pk)+"#comment="+str(editingComment.pk))
        else:
            #Form errors
            return render_to_response('editcommentform.html', dict(form=form, projectpk=pk, comment_id=editingComment.pk))
    else:
        #Fill form with the users comment!
        form = commentForm()
        from django import forms
        form.fields['parent'].widget = forms.HiddenInput()
        form.fields['parent'].initial = editingComment.parent
        form.fields['commenttext'].initial = editingComment.commenttext
        c=dict(form=form, projectpk=pk, comment_id=editingComment.pk)
        c.update(csrf(request))
        return render_to_response('editcommentform.html',c)
