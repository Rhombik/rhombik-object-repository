from django.utils.translation import ugettext_lazy as _

from taggit.forms import TagField
from taggit.managers import TaggableManager as BaseTaggableManager

from widgets import TagAutocomplete


class TaggableManager(BaseTaggableManager):
    def formfield(self, form_class=TagField, **kwargs):
        defaults = {
            "label": _("Tags"),
            "help_text": _("A comma-separated list of tags."),
            "required": not self.blank,
        }
        defaults.update(kwargs)

        defaults['widget'] = TagAutocomplete

        return form_class(**defaults)

# South introspection rule
try:
    from south.modelsinspector import add_ignored_fields
    add_ignored_fields(["^taggit_autocomplete\.managers"])
except ImportError:
    pass
