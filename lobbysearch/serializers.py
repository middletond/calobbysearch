from rest_framework import serializers

from bills.serializers import BillSerializer
from .models import Activity

class ActivitySerializer(serializers.ModelSerializer):
    matching_bills = BillSerializer(many=True, read_only=True)
    bills = BillSerializer(many=True, read_only=True)

    class Meta:
        model = Activity
        fields = (
            "filing_id",
            "amendment_id",
            "transaction_id",
            "filing_url",
            "form_type",
            "entity_code",
            "filing_date",
            "filer",
            "filer_id",
            "filer_url",
            "filer_last_name",
            "filer_first_name",
            "lobbyer",
            "lobbyer_id",
            "lobbyer_url",
            "lobbyer_last_name",
            "lobbyer_first_name",
            "lobbyer_city",
            "lobbyer_state",
            "lobbyer_zip",
            "lobbyer_phone",
            "employer",
            "employer_id",
            "employer_url",
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
            "matching_bills",
            "bills",
        )

    def __init__(self, *args, **kwargs):
        self.bill_query = kwargs.pop("bill_query", None)
        super(ActivitySerializer, self).__init__(*args, **kwargs)

    def to_representation(self, instance):
        if not hasattr(instance, "matching_bills"):
            instance.matching_bills = instance.bills.search(self.bill_query)
        return super(ActivitySerializer, self).to_representation(instance)
