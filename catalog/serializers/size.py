from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer
from rest_framework.serializers import ModelSerializer

from catalog.models import Size, TradeOffer


class SizeSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Size)

    class Meta:
        model = Size
        fields = ["id", "translations", "display_on_main"]
        read_only_fields = fields


class TradeOfferSizeSerializer(ModelSerializer):
    size = SizeSerializer()

    class Meta:
        model = TradeOffer
        fields = ["size", "amount", "id"]
        read_only_fields = fields
