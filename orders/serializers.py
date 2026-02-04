# apps/orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source="product.title", read_only=True)
    product_price = serializers.DecimalField(source="product.price", max_digits=10, decimal_places=2, read_only=True)
    category_name = serializers.CharField(source="product.category.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "product",          # product ID
            "product_title",    # title
            "product_price",    # price
            "category_name",    # category
            "quantity_requested"
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "created_at",
            "items",
            "total_items"
        ]

    def get_total_items(self, obj):
        return sum(item.quantity_requested for item in obj.items.all())



