from django.conf.urls import *
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = patterns("",
    url(r'^about/', TemplateView.as_view(template_name="about.html")),
)
