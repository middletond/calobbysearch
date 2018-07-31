from django.db import models

from bills import parser

from utils.session import Session
from utils import dates

DEFAULT_SEARCH_TYPE = "interests"
DEFAULT_DATE_FIELD = "start_date"

class ActivityQuerySet(models.QuerySet):
    """Queryset for `Activity` model."""

    def search(self, interest=None, company=None, bill=None,
               start=None, end=None, session=None, latest_only=True):
        # default to latest session if no date params
        if not(start or end or session):
            start, end = Session().as_dates()
        elif session: # session takes precedence over start / end
            start, end = Session(session).as_dates();
        # filter down by date ranges
        acts = self.dates(start, end)
        # filter down by text queries
        if interest:
            acts = acts.with_interest(interest)
        if company:
            acts = acts.with_company(company)
        if bill:
            acts = acts.with_bill(bill)
        if latest_only:
            acts = acts.latest_only()
        return acts

    def with_interest(self, query):
        return self.filter(interests__icontains=query)

    def with_company(self, query):
        return self.filter(involved_entities__icontains=query)

    def with_bill(self, query):
        # XXX: perhaps we should search Bill model directly, then grab act IDs from related?
        bill_names = parser.parse(query)
        if bill_names: # there are names, so search by that
            return self.filter(bills__name__in=bill_names)
        # else assume text / keyword query and search full names
        return self.filter(bills__full_name__iregex="\y{}\y".format(query))

    def dates(self, start=None, end=None):
        if not start:
            start = dates.BEGINNING_OF_TIME
        if not end:
            end = dates.today()
        return self.between(start, end)

    def latest_only(self):
        return self.distinct("filing_id")

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
    def connect_to_bills(self):
        """Parses bill names from activity interests and creates M2M connections."""
        connected_bills = []
        connected_acts = []
        acts = self.exclude(interests="")
        # chunk by session as this is some heavy lifting
        # NOTE: takes about 5 mins per session. I'd like to try celery w this.
        # for now only connecting latest session for expediency
        for sesh, verbose_sesh in Session.available_choices()[:1]:
            session_acts = acts.session(sesh)
            act_count = session_acts.count()
            print("Connecting bills to {} acts for session {}".format(
                act_count, verbose_sesh))

            for index, act in enumerate(session_acts, 1):
                bills = act.find_related_bills()
                if bills:
                    print("{}: Act {} of {}".format(verbose_sesh, index, act_count))
                    print("--- {} bills found.".format(bills.count()))
                    act.bills.add(*bills)
                    connected_bills.extend(bills)
                    connected_acts.append(act)
        return (connected_acts, connected_bills)
