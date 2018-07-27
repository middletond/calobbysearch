from rest_framework import serializers
from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            "filing_id",
            "amendment_id",
            "transaction_id",
            "form_type",
            "entity_code",
            "filing_date",
            "filer_id",
            "filer_name",
            "filer_last_name",
            "filer_first_name",
            "lobbyer_id",
            "lobbyer_name",
            "lobbyer_last_name",
            "lobbyer_first_name",
            "lobbyer_city",
            "lobbyer_state",
            "lobbyer_zip",
            "lobbyer_phone",
            "employer_id",
            "employer_name",
            "employer_last_name",
            "employer_first_name",
            "employer_city",
            "employer_state",
            "employer_zip",
            "employer_phone",
            "type",
            "start_date",
            "end_date",
            "interests",
            "compensation",
            "reimbursement",
            "period_total",
            "session_total",
        )
