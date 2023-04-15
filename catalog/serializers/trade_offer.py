from rest_framework import serializers

from catalog.models import TradeOffer
from catalog.serializers.size import SizeSerializer


class TradeOfferInStockSerializer(serializers.ModelSerializer):
    size = SizeSerializer()

    class Meta:
        model = TradeOffer
        fields = ("size", "amount")
