#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils.safestring import mark_safe

from bills import parser
from bills.models import Bill
from .managers import ActivityQuerySet

from utils.session import Session

CALACCESS_FILING_URL = "http://cal-access.sos.ca.gov/PDFGen/pdfgen.prg?filingid={filing_id}&amendid={amendment_id}"
CALACCESS_FILER_URL = "http://cal-access.sos.ca.gov/Lobbying/Employers/Detail.aspx?id={filer_id}&view=activity"

ACTIVITY_FORM_TYPE_CHOICES = (
    ("F625", "F625"),
    ("F635", "F635")
)

ENTITY_CODE_CHOICES = (
    ("LEM", "Lobby Employer"),
    ("FRM", "Lobby Firm"),
)

ACTIVITY_TYPE_CHOICES = (
    ("inhouse", "In-house Lobbying"),
    ("firm", "Contracted Lobby Firm"),
    ("other", "Other Payments to Influence"),
)

class Activity(models.Model):
    """An amalgamated lobby activity report for one quarter (3 months).

       Data for this report is filed by both lobbyers (F625) and employers (F635).
       In the original filings, the entity data gets stored in different fields
       depending on which of these is filing. For example, when an employer
       files, the employer's address ends up under the fields meant for
       the hired lobby firm!

       The purpose of this model is to:

       1. connect basic filer information with the meaningful activity fields
          (payments, dates, employer interests), which in their original form
          exist in balkanized tables in the CAL-ACCESS data.
       2. normalize these fields so they are always consistent and intuitive,
          regardless of who the original filer was.

       By doing this, it can provide this basic picture of lobby activity:

       employer ->
       paid $$ amount ->
       to lobbyer ->
       to influence interests / bills ->
       during these dates
    """
    # Filing
    filing_id = models.IntegerField(
        db_index=True,
        db_column="filing_id",
    )
    amendment_id = models.IntegerField(
        db_index=True,
        db_column="amendment_id",
    )
    transaction_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        db_column="transaction_id",
    )
    form_type = models.CharField(
        max_length=4,
        choices=ACTIVITY_FORM_TYPE_CHOICES,
        blank=True,
        null=True,
        db_column="form_type",
    )
    entity_code = models.CharField(
        max_length=4, choices=ENTITY_CODE_CHOICES,
        blank=True,
        null=True,
        db_column="entity_code",
    )
    filing_date = models.DateField(
        null=True,
        db_column="filing_date",
    )
    filer_id = models.CharField(
        max_length=9,
        blank=True,
        null=True,
        db_column="filer_id",
    )
    filer_name = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        db_column="filer_name",
    )
    filer_last_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        db_column="filer_last_name",
    )
    filer_first_name = models.CharField(
        max_length=45,
        blank=True,
        null=True,
        db_column="filer_first_name",
    )
    # Lobbyer
    lobbyer_id = models.CharField(
        max_length=9,
        blank=True,
        null=True,
        db_column="lobbyer_id",
    )
    lobbyer_name = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        db_column="lobbyer_name",
    )
    lobbyer_last_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        db_column="lobbyer_last_name",
    )
    lobbyer_first_name = models.CharField(
        max_length=45,
        blank=True,
        null=True,
        db_column="lobbyer_first_name",
    )
    lobbyer_city = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        db_column="lobbyer_city",
    )
    lobbyer_state = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        db_column="lobbyer_state",
    )
    lobbyer_zip = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        db_column="lobbyer_zip",
    )
    lobbyer_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        db_column="lobbyer_phone",
    )
    # Employer
    employer_id = models.CharField(
        max_length=9,
        blank=True,
        null=True,
        db_column="employer_id",
    )
    employer_name = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        db_column="employer_name",
    )
    employer_last_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        db_column="employer_last_name",
    )
    employer_first_name = models.CharField(
        max_length=45,
        blank=True,
        null=True,
        db_column="employer_first_name",
    )
    employer_city = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        db_column="employer_city",
    )
    employer_state = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        db_column="employer_state",
    )
    employer_zip = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        db_column="employer_zip",
    )
    employer_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        db_column="employer_phone",
    )
    # Activity
    type = models.CharField(
        max_length=10,
        choices=ACTIVITY_TYPE_CHOICES,
        blank=True,
        null=True,
        db_column="type",
    )
    start_date = models.DateField(
        null=True,
        db_column="start_date",
    )
    end_date = models.DateField(
        null=True,
        db_column="end_date",
    )
    interests = models.CharField(
        max_length=400,
        blank=True,
        null=True,
        db_column="interests",
    )
    bills = models.ManyToManyField(
        Bill,
        blank=True,
        related_name="activities",
    )
    compensation = models.DecimalField(
        decimal_places=2,
        max_digits=14,
        null=True,
        db_column="compensation",
    )
    reimbursement = models.DecimalField(
        decimal_places=2,
        max_digits=14,
        null=True,
        db_column="reimbursement",
    )
    period_total = models.DecimalField(
        decimal_places=2,
        max_digits=14,
        null=True,
        db_column="period_total",
    )
    session_total = models.DecimalField(
        decimal_places=2,
        max_digits=14,
        null=True,
        db_column="session_total",
    )
    involved_entities = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        db_column="involved_entities"
    )
    involved_keywords = models.TextField(
        blank=True,
        null=True,
        db_column="involved_keywords"
    )
    objects = ActivityQuerySet.as_manager()

    class Meta:
        ordering = ("-filing_id", "employer_name", "lobbyer_name",)
        verbose_name_plural = "Activities"

    def __unicode__(self):
        return "({} - {}) {} ->{}-> {}".format(
            self.start_date.strftime("%m/%Y"),
            self.end_date.strftime("%m/%Y"),
            self.employer.strip(),
            self.period_total,
            self.lobbyer.strip(),
        )

    def __str__(self):
        return str(self.__unicode__())

    @property
    def filer(self):
        return self.filer_name
    @property
    def employer(self):
        return self.employer_name
    @property
    def lobbyer(self):
        return self.lobbyer_name
    @property
    def entities(self):
        return self.involved_entities
    @property
    def session(self):
        return Session.string_from_date(self.start_date)
    @property
    def filer_url(self):
        return CALACCESS_FILER_URL.format(filer_id=self.filer_id)
    @property
    def employer_url(self):
        if not self.employer_id: return None
        return CALACCESS_FILER_URL.format(filer_id=self.employer_id)
    @property
    def lobbyer_url(self):
        if not self.lobbyer_id: return None
        return CALACCESS_FILER_URL.format(filer_id=self.lobbyer_id)
    @property
    def filing_url(self):
        return CALACCESS_FILING_URL.format(filing_id=self.filing_id,
                                           amendment_id=self.amendment_id)
    def filed_by(self):
        return "employer" if self.form_type == "F635" else "lobbyer"

    def is_internal(self):
        """Checks whether lobbying type is internal versus contracted."""
        return self.type in ("inhouse", "other")

    def find_related_bills(self):
        """Return bills based on parsed interest field."""
        bill_names = parser.parse(self.interests)
        return Bill.objects.filter(
            session=self.session,
            name__in=bill_names,
        )

    def populate_keywords(self, bills=[]):
        """Add bill names:titles plus raw interest text to `involved_keywords`."""
        self.involved_keywords = "{interests} {bill_titles}".format(
            interests=self.interests,
            bill_titles=", ".join(bill.full_name for bill in bills),
        ).strip()
        self.save()

    def source_link(self):
        return mark_safe(
            "<a href='{}' target='_blank'>Cal-Access Filings</a>".format(self.filing_url)
        )
    source_link.short_description = "Source"
