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
    updatecalaccess_began = models.DateTimeField(
        null=True,
        help_text="When `updatecalaccess` command began."
    )
    updatecalaccess_finished = models.DateTimeField(
        null=True,
        help_text="When `updatecalaccess` command finished."
    )
    loadactivities_began = models.DateTimeField(
        null=True,
        help_text="When `loadactivities` command began."
    )
    loadactivities_finished = models.DateTimeField(
        null=True,
        help_text="When `loadactivities` command finished."
    )
    loadbills_began = models.DateTimeField(
        null=True,
        help_text="When `loadbills` command began."
    )
    loadbills_finished = models.DateTimeField(
        null=True,
        help_text="When `loadbills` command finished."
    )
    connectbills_began = models.DateTimeField(
        null=True,
        help_text="When `connectbills` command began."
    )
    connectbills_finished = models.DateTimeField(
        null=True,
        help_text="When `connectbills` command finished."
    )
