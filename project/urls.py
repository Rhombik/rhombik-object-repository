from django.conf.urls import *
from django.conf import settings
from djangoratings.views import AddRatingFromModel
from project.views import ratingCalc

urlpatterns = patterns("",
    #Controls the ratings
    #/project/$PROJECTID/vote/8 for downvote. /project/$PROJECTID/vote/1 for upvote
    url(r'project/(?P<object_id>\d+)/rate/(?P<score>\d+)/', 'project.views.ratingCalc', {
        'app_label': 'project',
        'model': 'project',
        'field_name': 'rating',
    }),
    (r'^project/(.*)/thingtracker/$', 'project.views.thingtracker'),

    (r'^project/(.*)/$', 'project.views.project'),
    #for debugging search index tempalte
    (r'^test/$', 'project.views.searchtest'),

)
