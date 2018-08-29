from django.db import models
from django.contrib.humanize.templatetags.humanize import naturaltime

from utils import dates

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
    # Update calaccess
    updatecalaccess_began = models.DateTimeField(
        null=True,
        help_text="When `updatecalaccess` command began."
    )
    updatecalaccess_finished = models.DateTimeField(
        null=True,
        help_text="When `updatecalaccess` command finished."
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
    # Load bills
    loadbills_began = models.DateTimeField(
        null=True,
        help_text="When `loadbills` command began."
    )
    loadbills_finished = models.DateTimeField(
        null=True,
        help_text="When `loadbills` command finished."
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

    class Meta:
        ordering = ("-began", "-finished",)
        get_latest_by = "began"

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
