#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models

from .querysets import ActivityQuerySet

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
    objects = ActivityQuerySet.as_manager()

    class Meta:
        ordering = ("-filing_id", "-amendment_id", "type", "-period_total",)

    @property
    def employer(self):
        return self.employer_name
    @property
    def lobbyer(self):
        return self.lobbyer_name
    @property
    def entities(self):
        return self.involved_entities



# class Registration(models.Model):
#     pass


# class Bill(models.Model):
#     """A bill to be lobbied, parsed from `Activity.interest` fields. """
#     type = models.CharField(
#         max_length=4,
#         choices=BILL_TYPE_CHOICES,
#     )
#     number = models.IntegerField(
#
#     )
#     title = models.CharField(
#         max_length=250,
#         blank=True,
#         null=True,
#     )
#     name = models.CharField( # "{TYPE} {NUMBER}", for searching
#         max_length=10,
#         blank=True,
#         null=True,
#     )
#     full_name = models.CharField( # "{TYPE} {NUMBER} {TITLE}", for searching
#         max_length=300,
#         blank=True,
#         null=True,
#     )
#     description = models.TextField( # latest scraped bill analysis?
#         blank=True,
#         null=True,
#     )
#     text = models.TextField( # offical text -- also requires scraping
#         blank=True,
#         null=True,
#     )
#     session = models.CharField(
#         choices=SESSION_CHOICES,
#     )
#
#     def save(self, *args, **kwargs):
#         if not self.name:
#             self.name = "{0} {1} {2}".format(self.type, self.number, self.title)
#         super(self, Bill).save(*args, **kwargs)
