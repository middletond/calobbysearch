from django.db import models

from scrape import leginfo
from . import parser

class BillQuerySet(models.QuerySet):
    """Queryset for `Bill` model."""

    def search(self, query):
        bill_names = parser.parse(query)
        if bill_names: # there are names, so search by that
            return self.filter(name__in=bill_names)
        # else assume text / keyword query and search full names
        return self.filter(full_name__iregex="\y{}(s?)\y".format(query))


class BillManager(models.Manager):
    """Manager for `Bill` model."""

    def fetch(self):
        """Fetch latest bill records from leginfo government website."""
        return leginfo.bill_names.run()

    def load(self, records=[], clear_existing=True):
        """Load bills by passed records, else by scraping leginfo website."""
        if not records: records = self.fetch()

        if records and clear_existing:
            self.all().delete()
        # `bulk_create` doesn't call `save` so we normalize explicitly here
        bills = [self.model(**rec).normalize() for rec in records]
        return self.bulk_create(bills)

    # Queryset methods
    def get_queryset(self):
        return BillQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)
