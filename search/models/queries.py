from django.db import models

from lobbying.models import Activity
from .. import report, settings
from utils.session import Session
from utils import slack

from service import settings as service_settings

class Search(models.Model):
    """A single search of lobby data.

    """
    SEARCH_TYPE_CHOICES = ( # leaving room for more here, bills, registrations, etc
        ("activities", "Lobby Activities"),
        ("registrations", "Lobby Registrations"),
    )

    VALID_PARAMS = (
        "company",
        "interest",
        "bill",
        "start",
        "end",
        "session",
        "latest_only",
    )

    VALID_TEXT_PARAMS = (
        "company",
        "interest",
        "bill",
    )
    type = models.CharField(
        choices=SEARCH_TYPE_CHOICES,
        max_length=20,
        null=False,
    )
    company = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    interest = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    bill = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    start = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    end = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    session = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )
    latest_only = models.BooleanField(
        null=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    result_count = models.IntegerField(
        null=True
    )

    class Meta:
        ordering = ("-created",)
        get_latest_by = "created"
        verbose_name_plural = "Searches"

    @property
    def params(self):
        return { param: getattr(self, param)
                 for param in self.VALID_PARAMS
                 if getattr(self, param) }
    @property
    def text_params(self):
        return { k: v for k, v in self.params.items() if k in self.VALID_TEXT_PARAMS }

    def results(self):
        params = self.params
        res = Search.activities(**params)
        self.result_count = len(res)
        self.save()
        if settings.REPORT_SEARCH_RAN:
            report.search_ran(self)
        return res

    @staticmethod
    def activities(interest=None, company=None, bill=None,
                   start=None, end=None, session=None, latest_only=True):
        # default to latest session if no date params
        if not(start or end or session):
            start, end = Session().as_dates()
        elif session: # session takes precedence over start / end
            start, end = Session(session).as_dates();
        # filter down by date ranges
        acts = Activity.objects.dates(start, end)
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

    @staticmethod
    def registrations(self, interest=None, company=None, bill=None,
                      start=None, end=None, session=None, latest_only=True):
        return [] # for future etc

    def get_admin_list_url(self):
        return service_settings.CUR_HOST + "/admin/search/search/"
