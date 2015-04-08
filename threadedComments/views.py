
from threadedComments.models import Comment
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.contenttypes.models import ContentType
from threadedComments.forms import commentForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect,requires_csrf_token
from django.core.context_processors import csrf
from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponseForbidden
from threadedComments.models import Comment

def comment(request, content_type, content_pk, parent_id=None, comment_id=None):

    #make sure the user is logged in.
    if not request.user:
        return HttpResponseForbidden

    object_type = ContentType.objects.get(model=content_type).model_class()

    #Make sure the thing we're commenting on still exists.
    get_object_or_404(object_type, pk=content_pk)

    if comment_id != "new":
        commentInstance = get_object_or_404(Comment, pk=comment_id)
    else: #If it equals new.
        commentInstance = Comment()
        commentInstance.parent=get_object_or_404(Comment, pk=parent_id)

    #make sure we own the comment.
    if commentInstance.pk and commentInstance.commenter != request.user:
        return HttpResponseForbidden

    if request.method == 'POST':
        form = commentForm(request.POST)
        if request.POST['action'] == "Submit":
            if not form.is_valid():
                return render(request, 'commentform.html', dict(form=form, content_pk=pk))
            commentInstance.commenttext=form.cleaned_data['commenttext']
            commentInstance.commenter=request.user
            commentInstance.save()
        if request.POST['action'] == "Delete":
            commentInstance.delete()

        if request.POST['action'] == "Cancel":
            pass

        if "next" in request.GET and request.GET["next"]:
            return redirect(request.GET['next'])
        return redirect("/")

    else:
        form = commentForm(initial={"commenttext":commentInstance.commenttext})
        return render(request, 'commentform.html', dict(form=form, pk=content_pk, parent_id=parent_id))

