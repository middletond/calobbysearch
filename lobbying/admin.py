from django.contrib import admin
from . import models

@admin.register(models.Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin for lobby activity."""
    list_display = (
        "filing_id",
        "type",
        "employer",
        "compensation",
        "lobbyer",
        "interests",
        "start_date",
        "end_date",
        "filing_date",
        "filed_by",
        "source_link",
    )
    list_filter = (
        "start_date",
        "end_date",
        "form_type",
        "type",
    )
    search_fields = (
        "filing_id",
        "involved_entities",
        "interests",
    )
