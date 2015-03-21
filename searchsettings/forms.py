from django import forms

from haystack.forms import SearchForm
from taggit.utils import parse_tags
from project.models import Project
from taggit_autocomplete.widgets import TagAutocomplete
from haystack.query import SearchQuerySet


class objectSearchForm(SearchForm):
#    start_date = forms.DateField(required=False)
#    end_date = forms.DateField(required=False)
    tags = forms.CharField(widget=TagAutocomplete(attrs={'form':'searchForm'}),required=False)

    sortOPTIONS = (
        ("votes", "Votes"),
        ("new", "Newest"),
    )
    sort = forms.ChoiceField(choices=sortOPTIONS, required=False)

    timeOPTIONS = (
        ("everything", "all time"),
        ("year", "this year"),
        ("month", "this month"),
        ("week", "this week"),
        ("today", "today"),
    )
    From = forms.ChoiceField(choices=timeOPTIONS, required=False)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        if self.cleaned_data['q']:
            sqs = super(objectSearchForm, self).search()
        else:
            sqs= SearchQuerySet().exclude(draft=True)
  
        if not self.is_valid():
            return self.no_query_found()
        # Check to see if a start_date was chosen.
        if self.cleaned_data['tags']:
            sqs = sqs.filter(tags=parse_tags(self.cleaned_data['tags']))


#        if 'start_date' in self.cleaned_data:
#            sqs = sqs.filter(created__gte=self.cleaned_data['start_date'])

        # Check to see if an end_date was chosen.
#        if 'end_date' in self.cleaned_data:
#            sqs = sqs.filter(created=self.cleaned_data['end_date'])

        if not self.cleaned_data['sort'] or self.cleaned_data['sort'] == "votes":
            sqs = sqs.order_by('-ratingSortBest')
        elif self.cleaned_data['sort'] == "new":
            sqs = sqs.order_by('-created')

        return sqs
