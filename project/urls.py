from django.conf.urls import *
from django.conf import settings
from djangoratings.views import AddRatingFromModel
from project.views import ratingCalc

urlpatterns = patterns("",
    #Controls the ratings
    #/project/$PROJECTID/vote/1 for downvote. /project/$PROJECTID/vote/2 for upvote. 0 deletes your vote
    url(r'project/(?P<object_id>\d+)/vote/(?P<score>\d+)/', 'project.views.ratingCalc', {
        'app_label': 'project',
        'model': 'project',
        'field_name': 'rating',
    }),


    #A simple incrementer to count downloads.
    url(r'project/(?P<object_id>\d+)/downloadCountIncrement/(?P<score>\d+)/', AddRatingFromModel(), {
        'app_label': 'project',
        'model': 'project',
        'field_name': 'downloadcount',
    }),

## Comments!!!
    (r'^project/(?P<pk>\d+)/comment/(?P<comment_id>\d+)/$', 'comments.views.comment', {'content_type':'project'}),
    (r'^project/(?P<pk>\d+)/comment/$', 'comments.views.comment', {'content_type':'project'}),


    (r'^project/(.*)/thingtracker/$', 'project.views.thingtracker'),

    (r'^project/(.*)/$', 'project.views.project'),
    #for debugging search index tempalte
    (r'^test/$', 'project.views.searchtest'),

)
