from rest_framework.decorators import api_view,permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from stores.models import Store,Inventory
from .models import Order,OrderItem
from products.models import Product
from .serializers import OrderSerializer
from django.db import transaction
from django.shortcuts import get_object_or_404
from .tasks import send_order_confirmation



@api_view(['POST'])
@authentication_classes([])
def create_order(request):
    store_id = request.data.get("store_id")
    items = request.data.get("items", [])
    store = get_object_or_404(Store, id=store_id)

    with transaction.atomic():
        rejected = False
        for item in items:
            # inv = Inventory.objects.select_for_update().get(store=store, product_id=item["product_id"])
            inv = get_object_or_404(Inventory.objects.select_for_update(),store=store, product_id=item.get("product_id"))
            if inv.quantity < item["quantity_requested"]:
                rejected = True
                break

        status = Order.REJECTED if rejected else Order.CONFIRMED
        order = Order.objects.create(store=store, status=status)

        order_items = []
        for item in items:
            product = Product.objects.get(id=item["product_id"])
            order_items.append(
                OrderItem(
                    order=order,
                    product=product,
                    quantity_requested=item["quantity_requested"]
                )
            )
            if status == Order.CONFIRMED:
                inv = get_object_or_404(Inventory, store=store, product=product)
                inv.quantity -= item["quantity_requested"]
                inv.save()
        
        OrderItem.objects.bulk_create(order_items)
    
    send_order_confirmation.delay(order.id)


    serializer = OrderSerializer(order)
    return Response(serializer.data, status=201)


