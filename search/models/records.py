from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.humanize.templatetags.humanize import naturaltime

from utils import dates, slack
from .. import settings

from service import settings as service_settings

COMMAND_BEGAN = "began"
COMMAND_FINISHED = "finished"
COMMAND_SUCCEEDED = "succeeded"
COMMAND_FAILED = "failed"
COMMAND_RESULT = "count"

COMMANDS = (
    "updatecalaccess",
    "loadactivities",
    "loadbills",
    "connectbills",
)

class PopulationAttempt(models.Model):
    """An attempt to populate the database with the latest lobby records.

    """
    began = models.DateTimeField(
        null=True,
        help_text="When the load attempt began."
    )
    finished = models.DateTimeField(
        null=True,
        help_text="When the load attempt finished."
    )
    succeeded = models.NullBooleanField(
        default=None,
        verbose_name=" ",
        help_text="Whether the load attempt succeeded."
    )
    reason = models.CharField(
        max_length=250,
        null=True,
        verbose_name="Failures",
        help_text="The reasons for a failure."
    )
    # Update calaccess
    updatecalaccess_began = models.DateTimeField(
        null=True,
        help_text="When `updatecalaccess` command began."
    )
    updatecalaccess_finished = models.DateTimeField(
        null=True,
        help_text="When `updatecalaccess` command finished."
    )
    updatecalaccess_succeeded = models.NullBooleanField(
        default=None,
        verbose_name=" ",
        help_text="Whether `updatecalaccess` command succeeded."
    )
    # Load activities
    loadactivities_began = models.DateTimeField(
        null=True,
        help_text="When `loadactivities` command began."
    )
    loadactivities_finished = models.DateTimeField(
        null=True,
        help_text="When `loadactivities` command finished."
    )
    loadactivities_succeeded = models.NullBooleanField(
        default=None,
        verbose_name=" ",
        help_text="Whether `loadactivities` command succeeded."
    )
    loadactivities_count = models.IntegerField(
        null=True,
        verbose_name="Acts Loaded",
        help_text="Count of activities loaded."
    )
    # Load bills
    loadbills_began = models.DateTimeField(
        null=True,
        help_text="When `loadbills` command began."
    )
    loadbills_finished = models.DateTimeField(
        null=True,
        help_text="When `loadbills` command finished."
    )
    loadbills_succeeded = models.NullBooleanField(
        default=None,
        verbose_name=" ",
        help_text="Whether `loadbills` command succeeded."
    )
    loadbills_count = models.IntegerField(
        null=True,
        verbose_name="Bills Loaded",
        help_text="Count of bills loaded."
    )
    # Connect bills to activities
    connectbills_began = models.DateTimeField(
        null=True,
        help_text="When `connectbills` command began."
    )
    connectbills_finished = models.DateTimeField(
        null=True,
        help_text="When `connectbills` command finished."
    )
    connectbills_succeeded = models.NullBooleanField(
        default=None,
        verbose_name=" ",
        help_text="Whether `connectbills` command succeeded."
    )
    connectedbills_count = models.IntegerField(
        null=True,
        verbose_name="Bills Connected",
        help_text="Count of bills connected."
    )
    connectedacts_count = models.IntegerField(
        null=True,
        verbose_name="Acts Connected",
        help_text="Count of acts connected."
    )
    class Meta:
        ordering = ("-began", "-finished",)
        get_latest_by = "began"

    @property
    def status(self):
        if self.succeeded == None:
            return "In-progress"
        if self.succeeded == True:
            return "Succeeded"
        if self.succeeded == False:
            return "Failed"

    def get_admin_list_url(self):
        return service_settings.CUR_HOST + "/admin/search/populationattempt/"

    def begin(self):
        self.began = timezone.now()
        self.save()
        if settings.NOTIFY_ON_POPULATION_BEGIN:
            self.notify(COMMAND_BEGAN)

    def finish(self):
        self.finished = timezone.now()
        self.succeeded = True
        self.save()
        if settings.NOTIFY_ON_POPULATION_FINISH:
            self.notify(COMMAND_FINISHED)

    def notify(self, event):
        headline = "Population attempt #{} just {}.".format(self.id, event)
        url = self.get_admin_list_url()
        details = slack.attachment("details", {
            "Status": self.status,
            "Took": self.took(),
            "Began At": self.began,
            "Finished At": self.finished,
            "Updating Calaccess Took": self.updatecalaccess_took(),
            "Loading Activities Took": self.loadactivities_took(),
            "Loading Bills Took": self.loadbills_took(),
            "Connecting Bills Took": self.connectbills_took(),
            "Failures": self.reason,
        }, url=url)
        stats = slack.attachment("stats", {
            "Activities Loaded": self.loadactivities_count,
            "Bills Loaded": self.loadbills_count,
            "Activities Connected": self.connectedacts_count,
            "Bills Connected": self.connectedbills_count,
        }, url=url)
        return slack.message(headline, [details, stats])

    def log(self, command, event, outcome=None):
        if event == COMMAND_BEGAN:
            self.log_timestamp(command, event)
        if event == COMMAND_FAILED:
            self.log_failure(command, event, outcome)
        if event == COMMAND_SUCCEEDED:
            self.log_success(command, event, outcome)

    def log_success(self, command, outcome=None):
        self.log_timestamp(command, COMMAND_FINISHED)
        self.log_status(command, succeeded=True)
        if outcome:
            self.log_count(command, outcome)
        self.save()

    def log_failure(self, command, outcome=None):
        self.log_status(command, succeeded=False)
        if outcome:
            self.reason = "{}: {}".format(command, outcome)
        self.save()

    def log_timestamp(self, command, event):
        timestamp_field = "{}_{}".format(command, event)
        if hasattr(self, timestamp_field):
            setattr(self, timestamp_field, timezone.now())
        self.save()

    def log_status(self, command, succeeded):
        status_field = "{}_{}".format(command, COMMAND_SUCCEEDED)
        if hasattr(self, status_field):
            setattr(self, status_field, succeeded)

    def log_count(self, command, count):
        if command == "updatecalaccess":
            pass
        elif command == "loadactivities":
            self.loadactivities_count = count
        elif command == "loadbills":
            self.loadbills_count = count
        elif command == "connectbills":
            self.connectedacts_count = count[0]
            self.connectedbills_count = count[1]
        self.save()

    def took(self, command=None):
        began, finished = self.began, self.finished
        if command:
            began = getattr(self, "{}_began".format(command))
            finished = getattr(self, "{}_finished".format(command))
        if not (began or finished):
            return ""
        if not finished:
            return "began " + naturaltime(began)
        return dates.humanize_delta(finished - began)

    def updatecalaccess_took(self):
        return self.took("updatecalaccess")

    def loadactivities_took(self):
        return self.took("loadactivities")

    def loadbills_took(self):
        return self.took("loadbills")

    def connectbills_took(self):
        return self.took("connectbills")
