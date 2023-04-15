from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer
from rest_framework import serializers

from catalog.models import Category
from utils.files.serializers import CropImageFieldSerializer


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        print(value)
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ParentCategorySerializer(serializers.ModelSerializer):
    translations = TranslatedFieldsField(shared_model=Category)

    class Meta:
        model = Category
        fields = ["translations", "slug"]


class CategoryBaseSerializer(TranslatableModelSerializer):
    cover = CropImageFieldSerializer("1050x1400", options={"crop": "center"})
    translations = TranslatedFieldsField(shared_model=Category)

    class Meta:
        model = Category
        fields = ["translations", "cover", "slug", "order"]
        read_only_fields = fields


class CategoryInMenuSerializer(TranslatableModelSerializer):
    cover = CropImageFieldSerializer("1920x1080", options={"crop": "center"})
    translations = TranslatedFieldsField(shared_model=Category)

    class Meta:
        model = Category
        fields = ["translations", "cover", "slug", "cover_title", "cover_description"]
        read_only_fields = fields


class SmallCategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Category)

    class Meta:
        model = Category
        fields = ["translations", "slug"]
        read_only_fields = fields


class CategorySerializer(CategoryBaseSerializer):
    children = RecursiveField(read_only=True, many=True)
    parent = ParentCategorySerializer()

    class Meta(CategoryBaseSerializer.Meta):
        model = Category
        fields = CategoryBaseSerializer.Meta.fields + ["parent", "children"]


class CategoryHeaderSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Category)
    children = RecursiveField(read_only=True, many=True)
    parent = ParentCategorySerializer()

    class Meta(CategoryBaseSerializer.Meta):
        model = Category
        fields = ["translations", "slug", "parent", "children", "order"]


class CategoryBlock404Serializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Category)
    parent = ParentCategorySerializer()
    children = RecursiveField(read_only=True, many=True)
    cover = CropImageFieldSerializer("1050x1400", options={"crop": "center"})

    class Meta(CategoryBaseSerializer.Meta):
        model = Category
        fields = ["translations", "slug", "parent", "children", "cover", "order"]
