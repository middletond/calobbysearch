from django.db import models
from clint.textui import progress

from bills import parser as bill_parser

from utils.session import Session
from utils import dates

from service import settings

class ActivityQuerySet(models.QuerySet):
    """Queryset for `Activity` model."""

    def with_interest(self, query):
        return self.filter(interests__icontains=query)

    def with_company(self, query):
        return self.filter(involved_entities__icontains=query)

    def with_bill(self, query):
        bill_names = bill_parser.parse(query)
        if bill_names: # there are bill names, so search by that
            return self.filter(bills__name__in=bill_names)
        # else assume text / keyword query and search full names
        return self.filter(bills__full_name__iregex="\y{}\y".format(query)) # XXX full text search here please?

    def has_interests(self):
        return self.exclude(interests="")

    def has_bills(self):
        return self.filter(bills__isnull=False)

    def between(self, start=None, end=None, field=None):
        if not start:
            start = dates.BEGINNING_OF_TIME
        if not end:
            end = dates.today()
        # results should include any activity range
        # that touches the start - end dates.
        # ex: 1/03/18 - 3/20/18 should return matches w dates 1/1/18 - 3/31/18
        return self.filter(
            end_date__gte=dates.parse(start),
            start_date__lte=dates.parse(end),
        )

    def session(self, session):
        return self.between(*Session(session).as_dates())

    def latest_only(self):
        UNIQUE_ACT_FIELDS = ("filing_id", "employer_name", "lobbyer_name", "type",)
        return self.order_by(*UNIQUE_ACT_FIELDS, "-amendment_id") \
                   .distinct(*UNIQUE_ACT_FIELDS)

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

        if settings.CONNECT_BILLS_DEBUG:
            acts = self.session(session).has_interests()[:settings.CONNECT_BILLS_DEBUG_LENGTH]
        else:
            acts = self.session(session).has_interests()
        act_count = acts.count()

        print("Connecting bills to {} acts for session {}".format(
            act_count, session))

        for act in progress.bar(list(acts)):
            bills = act.find_related_bills()
            if bills:
                # create M2M connections
                act.bills.add(*bills)
                # populate `involved_keywords` text field
                # with bill titles + act interests
                act.populate_keywords(bills)
                connected_bills.extend(bills)
                connected_acts.append(act)
        return (connected_acts, connected_bills)
