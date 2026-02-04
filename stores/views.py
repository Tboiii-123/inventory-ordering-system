from rest_framework.decorators import api_view,permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status

from .models import Store,Inventory
from orders.serializers import OrderSerializer

from django.shortcuts import get_object_or_404




from .serializers import InventoryListSerializer




@api_view(['GET'])

def list_store_orders(request, store_id):
    try:
        store = Store.objects.get(id=store_id)
    except Store.DoesNotExist:
        return Response(
            {"error": "Store not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Optimized query: prefetch items + product + category
    orders = store.orders.prefetch_related(
        "items__product__category"
    ).order_by("-created_at")
#  # Normal/unoptimized: just get orders
#     orders = store.orders.all().order_by("-created_at")

    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


# apps/stores/views.py
@api_view(["GET"])
def store_inventory(request, store_id):
    try:
        store = Store.objects.get(id=store_id)
    except Store.DoesNotExist:
        return Response(
            {"error": "Store not found."},
            status=status.HTTP_404_NOT_FOUND
        )


    inventory_qs =Inventory.objects.filter(store=store).select_related("product", "product__category").order_by("product__title")  # ✅ alphabetical sorting by title
    

    serializer = InventoryListSerializer(inventory_qs, many=True)
    return Response(serializer.data)


