from django.db.models import Q
from parler_rest.fields import TranslatedFieldsField
from rest_framework import serializers

from catalog.serializers import CategoryBlock404Serializer
from utils.models import CategoryBlock


class CategoryBlockSerializer(serializers.ModelSerializer):
    translations = TranslatedFieldsField(shared_model=CategoryBlock)
    category = serializers.SerializerMethodField()

    class Meta:
        model = CategoryBlock
        fields = ["slug", "category", "translations"]

    def get_category(self, obj: CategoryBlock):
        return CategoryBlock404Serializer(
            obj.category.filter(Q(is_active=True) & ~Q(Q(cover="") | Q(cover=None))), context=self.context, many=True
        ).data
