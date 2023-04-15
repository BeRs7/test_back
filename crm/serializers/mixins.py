from rest_framework import serializers

from catalog.models import Product


class ItemsToActionSerializer(serializers.Serializer):
    items_to_action = serializers.ListField(required=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "order")
