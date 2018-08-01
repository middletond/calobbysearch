from django.db import models

from .managers import BillManager
from .parser import parse_type, parse_number, parse_one

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

TITLE_MAX_LENGTH = 250

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
        blank=True,
        null=True,
    )
    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
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
    # metadata
    url = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    normalized = models.BooleanField(
        default=False,
    )

    objects = BillManager()

    def __unicode__(self):
        return "{} {}: {}".format(self.session, self.name, self.title)

    def __str__(self):
        return str(self.__unicode__())

    def normalize(self):
        self.name = parse_one(self.name) # coerce to correct format
        if not self.type:
            self.type = parse_type(self.name)
        if not self.number:
            self.number = parse_number(self.name)
        if not self.title:
            self.title = ""
        if len(self.title) > TITLE_MAX_LENGTH:
            self.title = self.title[:TITLE_MAX_LENGTH]
        if not self.full_name:
            self.full_name = "{0} {1} {2}".format(self.type, self.number, self.title)
        self.normalized = True
        return self

    def save(self, *args, **kwargs):
        if not self.normalized:
            self.normalize()
        super(Bill, self).save(*args, **kwargs)
