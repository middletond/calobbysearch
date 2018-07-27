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
    }
    text_queries = {key: params[key] for key in TEXT_QUERIES if params[key]}
    if not text_queries:
        message = "Please include one or more text parameters to search for: "
        message += ", ".join(TEXT_QUERIES)
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    try:
        acts = Activity.objects.search(**params)
        pager = paginated(acts, request)
        serializer = ActivitySerializer(pager.page, many=True)
        return pager.get_paginated_response(serializer.data)
        # return Response(serializer.data)
    except ValueError as error:
        return Response(str(error), status=status.HTTP_400_BAD_REQUEST)


def paginated(queryset, request):
    paginator = PageNumberPagination()
    paginator.page_size = 2
    paginator.paginate_queryset(queryset, request)
    return paginator
