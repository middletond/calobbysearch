from django.contrib import admin
from . import models

@admin.register(models.PopulationAttempt)
class PopulationAttemptAdmin(admin.ModelAdmin):
    """Admin for load attempts."""
    list_display = (
        "began",
        "took",
        "updatecalaccess_took",
        "loadactivities_took",
        "loadbills_took",
        "connectbills_took",
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
