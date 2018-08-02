from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Activity
from .serializers import ActivitySerializer

TEXT_QUERIES = ("company", "interest", "bill")

@api_view(["GET"])
def search(request, format=None):
    """Search for lobby activities by interest, company, or bill.

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
        # meta
        "latest_only": True if int(request.GET.get("latest_only", True)) else False
    }
    text_queries = {key: params[key] for key in TEXT_QUERIES if params[key]}
    if not text_queries:
        message = "Please include one or more text parameters to search for: "
        message += ", ".join(TEXT_QUERIES)
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    try:
        acts = Activity.objects.search(**params)
        pager, page = paginated(acts, request)
        serializer = ActivitySerializer(page, many=True, bill_query=params["bill"])
        return pager.get_paginated_response(serializer.data)
    except ValueError as error:
        return Response(str(error), status=status.HTTP_400_BAD_REQUEST)


# refactor this into something better.
def paginated(queryset, request):
    paginator = PageNumberPagination()
    paginator.page_size = 100
    paginator.paginate_queryset(queryset, request)
    return (paginator, paginator.page)
