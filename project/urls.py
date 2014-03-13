from django.conf.urls import *
from django.conf import settings
from updown.views import AddRatingFromModel

urlpatterns = patterns("",
    url(r"^(?P<object_id>\d+)/rate/(?P<score>[\d\-]+)$", AddRatingFromModel(), {
        'app_label': 'project',
        'model': 'project',
        'field_name': 'rating',
    }, name="video_rating"),
)
