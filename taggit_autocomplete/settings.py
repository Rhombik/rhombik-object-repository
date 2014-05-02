from django.conf import settings

# Both settings must be lists or tuples of URLs
CSS = getattr(settings, 'TAGGIT_AUTOCOMPLETE_CSS', ())
CSS = CSS + ('taggit_autocomplete/css/jquery.tagit.css', )
JS = getattr(settings, 'TAGGIT_AUTOCOMPLETE_JS', ())
JS = JS + ('taggit_autocomplete/js/tag-it.js', )
