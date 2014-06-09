from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

    url(r'^$', 'project.views.list', name='home'),

    # Examples:
    # url(r'^$', 'exampleSettings.views.home', name='home'),
    # url(r'^exampleSettings/', include('exampleSettings.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^edit/(.*)/$', 'project.views.edit'),
    (r'^create/$', 'project.views.create'),

    (r'^tag/(.*)/$', 'project.views.tag'),
    (r'^tagcloud/$', 'project.views.tagcloud' ),

    # Comments urls
    url(r'^articles/comments/', include('django.contrib.comments.urls')),

    #Search urls
    (r'^search/', include('searchsettings.urls')),

    #captcha urls
    url(r'^captcha/', include('captcha.urls')),

    (r'^login/$', 'userProfile.views.login_user'),
    (r'^logout/$', 'userProfile.views.logout_user'),
    (r'^register/$', 'userProfile.views.register'),
    (r'^legister/$', 'userProfile.views.legister'),
    (r'^editProfile/$', 'userProfile.views.edit'),

    #preview pages for the STL files.
    (r'^thumbs/jsc3d/(.*)', 'thumbnailer.views.stlthumb'),
    (r'^preview/jsc3d/(.*)', 'thumbnailer.views.stlview'),
    (r'', include('taggit_autocomplete.urls')),
    #user profile pages
    url(r'^userProfile/', include('userProfile.urls')),
    (r'^editUser/', 'userProfile.views.edit'),

    #We should try to move url definitions into each app
    url(r'', include('bootstrapTheme.urls')),
    url(r'', include('multiuploader.urls')),
    url(r'', include('project.urls')),
    url(r'', include('filemanager.urls')),


)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

