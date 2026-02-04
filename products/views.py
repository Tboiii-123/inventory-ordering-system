from rest_framework.decorators import api_view,throttle_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import F

from .serializers import ProductSearchSerializer
from search.utils import product_search_queryset,product_autocomplete
from .throttles import SearchThrottle

class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(["GET"])
def product_search(request):
    qs = product_search_queryset(request.GET)

    store_id = request.GET.get("store_id")
    if store_id:
        qs = qs.annotate(inventory_quantity=F("inventory__quantity"))

    paginator = ProductPagination()  
    paginated_qs = paginator.paginate_queryset(qs, request)

    if paginated_qs is not None:
        serializer = ProductSearchSerializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)
    else:
        # fallback if pagination fails
        serializer = ProductSearchSerializer(qs, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@throttle_classes([SearchThrottle])
def product_suggest(request):
  
    q = request.GET.get("q", "").strip()

    suggestions = product_autocomplete(q)

    return Response({
        "query": q,
        "results": suggestions
    })
