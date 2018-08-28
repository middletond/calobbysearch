from django.db import models

class Search(models.Model):
    """A requested search of lobby data."""
    pass


class LoadAttempt(models.Model):
    """An attempt to load the latest lobby data into database.

    """
    began = models.DateTimeField(
        null=True,
        help_text="When the load attempt began."
    )
    finished = models.DateTimeField(
        null=True,
        help_text="When the load attempt finished."
    )
    update_calaccess_began = models.DateTimeField(
        null=True,
        help_text="When `updatecalaccess` command began."
    )
    update_calaccess_finished = models.DateTimeField(
        null=True,
        help_text="When `updatecalaccess` command finished."
    )
    load_activities_began = models.DateTimeField(
        null=True,
        help_text="When `loadactivities` command began."
    )
    load_activities_finished = models.DateTimeField(
        null=True,
        help_text="When `loadactivities` command finished."
    )
    load_bills_began = models.DateTimeField(
        null=True,
        help_text="When `loadbills` command began."
    )
    load_bills_finished = models.DateTimeField(
        null=True,
        help_text="When `loadbills` command finished."
    )
    connect_bills_began = models.DateTimeField(
        null=True,
        help_text="When `connectbills` command began."
    )
    connect_bills_finished = models.DateTimeField(
        null=True,
        help_text="When `connectbills` command finished."
    )
