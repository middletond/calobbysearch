from django.db import models


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
