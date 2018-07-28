from django.db import models

class BillQuerySet(models.QuerySet):
    """Acting manager for `Bill` model."""

    def load(self):
        """Load bills by scraping leginfo"""
        pass

    def connect(self):
        """Connect bills to lobbysearch by parsing activity interests."""
        pass
