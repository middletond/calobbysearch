from django.db import models

from scrape import leginfo

class BillQuerySet(models.QuerySet):
    """Acting manager for `Bill` model."""

    def fetch(self):
        """Fetch latest bill records from leginfo government website."""
        return leginfo.bill_names.run()

    def load(self, records=[], clear_existing=True):
        """Load bills by passed records, else by scraping leginfo website."""
        if not records: records = self.fetch()
        
        if records and clear_existing:
            self.all().delete()
        return [self.create(**rec) for rec in records]

    def connect(self):
        """Connect bills to lobbysearch by parsing activity interests."""
        pass
