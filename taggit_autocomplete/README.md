django-taggit-jquery-tag-it
===========================

About
-----

This is a fork of django-taggit-autocomplete, which is in turn a fork of
django-tagging-autocomplete.

They can be found in:

* http://code.google.com/p/django-tagging-autocomplete/
* https://github.com/Jaza/django-taggit-autocomplete

This fork make uses of Tag-it! a jQuery UI plugin:

* https://github.com/aehlke/tag-it 

It enhances django-taggit by adding autocompletion and a nicer UI:

* https://github.com/alex/django-taggit

This app works also works with django-taggit-hvad, see:

* https://github.com/rasca/django-taggit-hvad

Installation
------------

1. We recomend using `pip` and `virtualenv`:

    pip install -e git+git@github.com:rasca/django-taggit-jquery-tag-it.git#egg=django-taggit-autocomplete

2. Add 'tagging_autocomplete' to INSTALLED_APPS in your project's `settings.py`
   file:

    INSTALLED_APPS = (

    'tagging',    
    'tagging\_autocomplete',

    \# ...

3. Add the following line in you project's `urls.py` file:

    (r'^taggit\_autocomplete/', include('taggit\_autocomplete.urls')),

4. You should provide jQuery and jQuery UI (and a theme). If they aren't
   available in the current context, set `TAGGIT_AUTOCOMPLETE_CSS` and
   `TAGGIT_AUTOCOMPLETE_JS` in your settings file. Both settings must be lists.

5. Enjoy

Usage
-----

The easiest solution is to user our subclass of taggit.managers.TaggableManager
in the tagged models.

Example:

    from django.db import models
    from taggit_autocomplete.managers import TaggableManager
    
    class SomeModel(models.Model):
        tags = TaggableManager()
