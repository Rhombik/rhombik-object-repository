from django.conf.urls import *
from django.conf import settings
from djangoratings.views import AddRatingFromModel


urlpatterns = patterns("",
    #Controls the ratings
    #/project/$PROJECTID/vote/8 for downvote. /project/$PROJECTID/vote/1 for upvote
    url(r'project/(?P<object_id>\d+)/rate/(?P<score>\d+)/', AddRatingFromModel(), {
        'app_label': 'project',
        'model': 'project',
        'field_name': 'rating',
    }),

    (r'^project/(.*)/$', 'project.views.project'),

)
