from django import forms

from taggit_autosuggest.widgets import TagAutoSuggest
from haystack.forms import SearchForm
from taggit.utils import parse_tags
from project.models import Project

class DateRangeSearchForm(SearchForm):
#    start_date = forms.DateField(required=False)
#    end_date = forms.DateField(required=False)
    tags = forms.CharField(widget=TagAutoSuggest,required=False)

    sortOPTIONS = (
    ("false", "Sort by nothing"),
    ("false", "Also sort by noting"),
    )
    sort = forms.ChoiceField(choices=sortOPTIONS)

    timeOPTIONS = (
    ("false", "all time"),
    ("false", "this year"),
    ("false", "this month"),
    ("false", "this week"),
    ("false", "today"),

    )
    From = forms.ChoiceField(choices=timeOPTIONS)


    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(DateRangeSearchForm, self).search()
        if not self.is_valid():
            return self.no_query_found()

        # Check to see if a start_date was chosen.
        if self.cleaned_data['tags']:
#            from taggit.models import tag
            sqs = sqs.filter(tags=parse_tags(self.cleaned_data['tags']))


        if self.cleaned_data['start_date']:
            sqs = sqs.filter(created__gte=self.cleaned_data['start_date'])

        # Check to see if an end_date was chosen.
        if self.cleaned_data['end_date']:
            sqs = sqs.filter(created=self.cleaned_data['end_date'])
        return sqs
