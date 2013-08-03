from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',

    (r'^post/(.*)/$', 'post.views.post'),

    #preview pages for the STL files.
    (r'^thumbs/stl/(.*)', 'thumbnailer.views.stlthumb'),
    (r'^preview/stl/(.*)', 'thumbnailer.views.stlview'),

    # Examples:
    # url(r'^$', 'exampleSettings.views.home', name='home'),
    # url(r'^exampleSettings/', include('exampleSettings.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
)


