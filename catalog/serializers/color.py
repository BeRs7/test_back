from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer

from catalog.models import Color, Product


class ColorSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Color)

    class Meta:
        model = Color
        fields = ["translations", "hex"]
        read_only_fields = fields

