from rest_framework import serializers

from .models import Bill

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = (
            "name",
            "title",
            "session",
            "url",
            "authors",
            "status",
        )
