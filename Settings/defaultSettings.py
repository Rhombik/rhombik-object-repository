# Django settings for exampleSettings project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)


import os
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

### stuff for the celery task queue



BROKER_URL = 'django://'
#Makes debugging easier. Don't use in production
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS =True
##Bullshit to make scrapy+celery work. Probably hugely innefficient for twisted reasons I don't understand.
CELERYD_MAX_TASKS_PER_CHILD = 1


MANAGERS = ADMINS

LOGIN_URL="legister"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'exampleSettings.sqlite3',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'searchsettings.celeryHaystack.celerySignalProcessor'
#HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.BaseSignalProcessor'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # default
    'guardian.backends.ObjectPermissionBackend',
)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

#Sets the url that phantomJS should use for all of its rendering. Must be an instance of the site.
URL = 'http://localhost:8000'
#the path to the phantomjs binary, properly escaped.
PHANTOMJSPATH = "phantomjs"

ANONYMOUS_USER_ID=-1
# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = PROJECT_PATH + '/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = PROJECT_PATH + '/static/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'static_precompiler.finders.StaticPrecompilerFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
  'django.core.context_processors.request',
  'django.contrib.auth.context_processors.auth',
)

##Github OAuth stuff. 'fraid you'll have to generate it yourself. These ones should work for debugging, but you'll have to edit your hosts file.
##If you're going to be working on this, feel free to message me ~traverseda

GIT_CLIENT_ID="7228e16a274bba8d8487"
GIT_CLIENT_SECRET="ba96e5cecb54a7ec3c269259712c679e24962cba"

#Let's try and cache the inline javascript so you don't need to generate it

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': PROJECT_PATH+'/django_cache',
    },
    'javascript': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': PROJECT_PATH+'/coffeecache',
    }

}


STATIC_PRECOMPILER_COMPILERS = (
    'static_precompiler.compilers.CoffeeScript',
    'static_precompiler.compilers.SCSS',
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

#if DEBUG ==True:
if False:
    MIDDLEWARE_CLASSES += ('Settings.BeautifulMiddleware.BeautifulMiddleware',)

ROOT_URLCONF = 'Settings.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'Settings.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'guardian',
    'haystack',
    'searchsettings',
    'thumbnailer',
    'project',
    'multiuploader',
    # disabling example theme, including instead boostrapTheme
    #'exampleTheme',
    'bootstrapTheme',
    'userProfile',
    'captcha',
    'filemanager',
    'organization',
    'avatarBot',
    'taggit',
    'taggit_autocomplete',
    'testcases',
    'djangoratings',
    'threadedComments',
    'scraper',
    'mptt',
    'kombu.transport.django',
#    'threadedcomments',
#    'django.contrib.comments',
    #So we can inline coffeescript
    'static_precompiler',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'gitHooks',
)

COMMENTS_APP = 'threadedcomments'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}



if False:
    # make all loggers use the console.
    for logger in LOGGING['loggers']:
        LOGGING['loggers'][logger]['handlers'] = ['console']

MULTI_FILE_DELETE_URL = 'multi_delete'
MULTI_IMAGE_URL = 'multi_image'
MULTI_IMAGES_FOLDER = 'multiuploader_images'

###  autorize the use of user profile I guess.... (spike, take a letter:   user profile . user profile . user profile         . user profile)
AUTH_PROFILE_MODULE = "userProfile.userProfile"
