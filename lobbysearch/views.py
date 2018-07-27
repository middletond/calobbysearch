from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Activity
from .serializers import ActivitySerializer

TEXT_QUERIES = ("company", "interest", "bill")

@api_view(["GET"])
def search(request, format=None):
    """Search for activities by interests, company, or bill.

    """
    errors = []
    params = {
        # text
        "company": request.GET.get("company", None),
        "interest": request.GET.get("interest", None),
        "bill": request.GET.get("bill", None),
        # dates
        "session": request.GET.get("session", None),
        "start": request.GET.get("start", None),
        "end": request.GET.get("end", None),
    }
    text_queries = {key: params[key] for key in TEXT_QUERIES if params[key]}
    if not text_queries:
        message = "Please include one or more text parameters to search for: "
        message += ", ".join(TEXT_QUERIES)
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    try:
        acts = Activity.objects.search(**params)
        serializer = ActivitySerializer(acts, many=True)
        return Response(serializer.data)
    except ValueError as error:
        return Response(str(error), status=status.HTTP_400_BAD_REQUEST)
