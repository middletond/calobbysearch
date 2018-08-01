from django.db import models

from scrape import leginfo
from . import parser

class BillManager(models.Manager):
    """Acting manager for `Bill` model."""

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
