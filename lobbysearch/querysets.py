from django.db import models

from utils.session import Session
from utils import dates

DEFAULT_SEARCH_TYPE = "interests"
DEFAULT_DATE_FIELD = "start_date"

class ActivityQuerySet(models.QuerySet):
    """Acting manager for `Activity` model."""

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
        # TODO: Add bill parser logic + Bill model
        return self.filter(interests__icontains=query)

    def dates(self, start=None, end=None):
        if not start:
            start = dates.BEGINNING_OF_TIME
        if not end:
            end = dates.today()
        return self.between(start, end)

    def latest_only(self):
        return self.distinct("filing_id")

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
