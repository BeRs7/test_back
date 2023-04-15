from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer
from rest_framework import serializers

from catalog.models import Color, Size, ProductTag
from catalog.models.specs import Material


class ColorFilterSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Color)

    class Meta:
        model = Color
        fields = ["id", "translations", "hex", "display_on_main"]
        read_only_fields = fields


class SizeFilterSerializer(serializers.ModelSerializer):
    translations = TranslatedFieldsField(shared_model=Size)

    class Meta:
        model = Size
        fields = ["id", "translations", "display_on_main"]
        read_only_fields = fields


class TagFilterSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=ProductTag)

    class Meta:
        model = ProductTag
        fields = ["id", "slug", "translations"]


class MaterialFilterSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Material)

    class Meta:
        model = Material
        fields = ["id", "translations"]
