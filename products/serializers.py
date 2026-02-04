from rest_framework import serializers
from .models import Product


class ProductSearchSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)
    inventory_quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "price",
            "category",
            "inventory_quantity",
        ]
