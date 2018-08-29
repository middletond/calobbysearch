from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from lobbying.models import Activity
from lobbying.serializers import ActivitySerializer
from .models import Search

@api_view(["GET"])
def search_activities(request, format=None):
    """Search for lobby activities by interest, company, or bill.

    """
    search = Search(
        type = "activities",
        # text
        company = request.GET.get("company", None),
        interest = request.GET.get("interest", None),
        bill = request.GET.get("bill", None),
        # dates
        session = request.GET.get("session", None),
        start = request.GET.get("start", None),
        end = request.GET.get("end", None),
        # meta
        latest_only = True if int(request.GET.get("latest_only", True)) else False
    )
    if not search.text_params:
        message = "To run a search, include one or more text parameters to search for: "
        message += ", ".join(Search.VALID_TEXT_PARAMS)
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    try:
        search.save()
        acts = search.results()
        pager, page = paginated(acts, request)
        serializer = ActivitySerializer(page, many=True, bill_query=search.bill)
        return pager.get_paginated_response(serializer.data)
    except ValueError as error:
        return Response(str(error), status=status.HTTP_400_BAD_REQUEST)

# refactor this into something better.
def paginated(queryset, request):
    paginator = PageNumberPagination()
    paginator.page_size = 500
    paginator.paginate_queryset(queryset, request)
    return (paginator, paginator.page)
