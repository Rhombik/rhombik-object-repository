from django import forms
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from taggit.utils import edit_string_for_tags
from taggit_autocomplete import settings


class TagAutocomplete(forms.TextInput):
    input_type = 'text'

    def render(self, name, value, attrs=None):
        list_view = reverse('taggit_autocomplete-list')
        if value is not None and not isinstance(value, basestring):
            value = edit_string_for_tags(
                    [o.tag for o in value.select_related("tag")])
        html = super(TagAutocomplete, self).render(name, value, attrs)

        # Activate tag-it in this field
        js = u"""
            <script type="text/javascript">
                (function($) {
                    $(document).ready(function() {
                        $("#%(id)s").tagit({
                            caseSensitive: false,
                            tagSource: function(search, showChoices) {
                                options = this;
                                $.getJSON("%(source)s", {
                                    q: search.term.toLowerCase()
                                }, function(data) {
                                    showChoices(options._subtractArray(data, options.assignedTags()));
                                });
                            }
                        });
                    });
                })(jQuery);
            </script>
            """ % ({
                'id': attrs['id'],
                'source': list_view
            })
        return mark_safe("\n".join([html, js]))

    class Media:
        css = {
            'all': settings.CSS,
        }
        js = settings.JS
        
