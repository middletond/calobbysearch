from django.contrib import admin
from . import models

@admin.register(models.PopulationAttempt)
class PopulationAttemptAdmin(admin.ModelAdmin):
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

@admin.register(models.Search)
class SearchAdmin(admin.ModelAdmin):
    """Admin for requested searches."""
    list_display = (
        "created",
        "company",
        "interest",
        "bill",
        "start",
        "end",
        "session",
        "latest_only",
    )
