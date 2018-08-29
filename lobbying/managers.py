from django.db import models
from clint.textui import progress

from bills import parser

from utils.session import Session
from utils import dates

DEFAULT_SEARCH_TYPE = "interests"
DEFAULT_DATE_FIELD = "start_date"

class ActivityQuerySet(models.QuerySet):
    """Queryset for `Activity` model."""

    def with_interest(self, query):
        return self.filter(interests__icontains=query)

    def with_company(self, query):
        return self.filter(involved_entities__icontains=query)

    def with_bill(self, query):
        bill_names = parser.parse(query)
        if bill_names: # there are names, so search by that
            return self.filter(bills__name__in=bill_names)
        # else assume text / keyword query and search full names
        return self.filter(bills__full_name__iregex="\y{}\y".format(query))

    def has_interests(self):
        return self.exclude(interests="")

    def has_bills(self):
        return self.filter(bills__isnull=False)

    def dates(self, start=None, end=None):
        if not start:
            start = dates.BEGINNING_OF_TIME
        if not end:
            end = dates.today()
        return self.between(start, end)

    def latest_only(self):
        UNIQUE_ACT_FIELDS = ("filing_id", "employer_name", "lobbyer_name", "type",)
        return self.order_by(*UNIQUE_ACT_FIELDS, "-amendment_id") \
                   .distinct(*UNIQUE_ACT_FIELDS)

    def session(self, session):
        return self.between(*Session(session).as_dates())

    # Dates and Times
    def between(self, start, end, field=None):
        if not field:
            field = DEFAULT_DATE_FIELD
        return self.filter(**{field + "__range": dates.inclusive_range(start, end)})

    def before(self, end, field=None):
        return self.between(dates.BEGINNING_OF_TIME, end, field)

    def after(self, start, field=None):
        return self.between(start, dates.today(), field)

    def date(self, date, field=None): # pass in a timestamp and get the whole day. can be date, datetime, string, obj, etc
        return self.between(date, date, field)

    def today(self, field=None):
        today = dates.today()
        return self.date(today, field)

    # Loading methods
    def connect_to_bills(self, session=None):
        """Parses bill names from activity interests and creates M2M connections."""
        connected_bills = []
        connected_acts = []

        if not session: # run all sessions if none passed
            for sesh in Session.available_sessions():
                bills, acts = self.connect_to_bills(sesh)
                connected_bills.extend(bills)
                connected_acts.extend(acts)
            return (connected_acts, connected_bills)

        acts = self.session(session).has_interests()[:100] # XXX TESTING ONLY
        # acts = self.session(session).has_interests()
        act_count = acts.count()

        print("Connecting bills to {} acts for session {}".format(
            act_count, session))

        for act in progress.bar(list(acts)):
            bills = act.find_related_bills()
            if bills:
                act.bills.add(*bills)
                connected_bills.extend(bills)
                connected_acts.append(act)
        return (connected_acts, connected_bills)
