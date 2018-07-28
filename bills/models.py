from django.db import models

from .managers import BillQuerySet

from utils.session import Session

# http://www.csun.edu/~hfdss003/atacp/supplements/fph1.html#link4
BILL_TYPE_CHOICES = (
    ("AB", "Assembly Bill"),
    ("SB", "Senate Bill"),

    ("ACA", "Assembly Constitutional Amendment"),
    ("SCA", "Senate Constitutional Amendment"),

    ("AJR", "Assembly Joint Resolution"),
    ("SJR", "Senate Joint Resolution"),
    ("ACR", "Assembly Concurrent Resolution"),
    ("SCR", "Senate Concurrent Resolution"),
    ("HR", "House Resolution"),
    ("SR", "Senate Resolution"),
)

SESSION_CHOICES = Session.available_choices()

class Bill(models.Model):
    """A bill to be lobbied from the California legislature.

       How bill data is acquired:
       1. A list of all bills and their basic data is loaded by scraping
          leginfo.legislature.ca.gov
       2. Bills are connected to lobbying by parsing bill names from the
          `interests` field in `lobbysearch.Activity` records. """
    # basics
    type = models.CharField(
        max_length=3,
        choices=BILL_TYPE_CHOICES,
    )
    number = models.IntegerField(

    )
    title = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    name = models.CharField( # "{TYPE} {NUMBER}", for searching
        max_length=10,
        blank=True,
        null=True,
    )
    full_name = models.CharField( # "{TYPE} {NUMBER} {TITLE}", for searching
        max_length=300,
        blank=True,
        null=True,
    )
    # authors
    authors = models.CharField( # Text field for now. Scrape from leginfo list page
        max_length=250,
        blank=True,
        null=True,
    )
    coauthors = models.CharField( # Scrape from leginfo details page
        max_length=250,
        blank=True,
        null=True,
    )
    # text
    sections = models.CharField( # leginfo details page
        max_length=200,
        blank=True,
        null=True,
    )
    text = models.TextField( # actual offical text -- leginfo details
        blank=True,
        null=True,
    )
    digest = models.TextField( # legislative counsel digest - leginfo details
        blank=True,
        null=True,
    )
    analysis = models.TextField( # latest scraped bill analysis. should probably make FK model
        blank=True,
        null=True
    )
    # dates
    introduction_date = models.DateField( # leginfo details page
        blank=True,
        null=True,
    )
    session = models.CharField(
        max_length=8,
        choices=SESSION_CHOICES,
    )
    objects = BillQuerySet.as_manager()

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = "{0} {1} {2}".format(self.type, self.number, self.title)
        super(self, Bill).save(*args, **kwargs)