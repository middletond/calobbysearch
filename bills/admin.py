from django.contrib import admin
from . import models

@admin.register(models.Bill)
class BillAdmin(admin.ModelAdmin):
    """Admin for bills."""
    list_display = (
        "name",
        "title",
        "session",
        "introduction_date",
        "authors",
        "status",
        "source_link",
    )
    list_filter = (
        "type",
        "session",
        "introduction_date",
    )
    search_fields = (
        "full_name",
        "authors",
        "status",
    )
