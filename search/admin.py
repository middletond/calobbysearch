from django.contrib import admin
from . import models

@admin.register(models.LoadAttempt)
class LoadAttemptAdmin(admin.ModelAdmin):
    """Admin for load attempts."""
    list_display = (
        "began",
        "updatecalaccess_began",
        "updatecalaccess_finished",
        "loadactivities_began",
        "loadactivities_finished",
        "loadbills_began",
        "loadbills_finished",
        "connectbills_began",
        "connectbills_finished",
        "finished",
    )
