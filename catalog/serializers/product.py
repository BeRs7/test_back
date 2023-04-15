from django.db.models import Q
from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer
from rest_framework import serializers

from catalog.models import Product, ProductTag
from catalog.serializers.categories import CategorySerializer, SmallCategorySerializer
from catalog.serializers.color import ColorSerializer
from catalog.serializers.images import ImageSerializer
from catalog.serializers.size import TradeOfferSizeSerializer


class ProductTagSerializer(serializers.ModelSerializer):
    """Сермайлайзер тегов товаров"""

    translations = TranslatedFieldsField(shared_model=ProductTag)

    class Meta:
        model = ProductTag
        fields = ["translations", "slug"]


class ProductSmallTranslationsSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Product
        fields = ("name",)


class ProductColorSerializer(TranslatableModelSerializer):
    color = ColorSerializer()
    translations = TranslatedFieldsField(serializer_class=ProductSmallTranslationsSerializer, shared_model=Product)
    images = ImageSerializer(many=True)
    major_category = SmallCategorySerializer(many=False, read_only=True)
    tags = ProductTagSerializer(many=True)

    class Meta:
        model = Product
        fields = ["slug", "color", "images", "translations", "tags", "major_category"]
        read_only_fields = fields


class ProductListSerializer(TranslatableModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    translations = TranslatedFieldsField(shared_model=Product, read_only=True)
    seo_tags = ProductTagSerializer(many=True, read_only=True)
    exists_in_favorites = serializers.SerializerMethodField()
    color = ColorSerializer()
    tags = ProductTagSerializer(many=True)
    colors = ProductColorSerializer(many=True, read_only=True)
    major_category = SmallCategorySerializer(many=False, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "slug",
            "images",
            "price",
            "price_with_sale",
            "translations",
            "seo_tags",
            "tags",
            "is_new",
            "exists_in_favorites",
            "color",
            "colors",
            "major_category",
        ]

        read_only_fields = fields

    def get_exists_in_favorites(self, obj: Product):
        return obj.id in (
            self.context["request"].session.get("favorites")
            if self.context["request"].session.get("favorites")
            else []
        )


class ProductDetailSerializer(TranslatableModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    translations = TranslatedFieldsField(shared_model=Product, read_only=True)
    category = CategorySerializer(many=True, read_only=True)
    tags = ProductTagSerializer(many=True, read_only=True)
    seo_tags = ProductTagSerializer(many=True, read_only=True)
    color = ColorSerializer(read_only=True)
    colors = ProductColorSerializer(many=True, read_only=True)
    sizes = serializers.SerializerMethodField()
    exists_in_favorites = serializers.SerializerMethodField()
    total_look = ProductListSerializer(many=True, read_only=True)
    major_category = SmallCategorySerializer(many=False, read_only=True)
    suggested_products = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "images",
            "translations",
            "category",
            "major_category",
            "color",
            "colors",
            "sizes",
            "tags",
            "seo_tags",
            "slug",
            "weight",
            "is_new",
            "price",
            "price_with_sale",
            "exists_in_favorites",
            "total_look",
            "suggested_products",
        ]

        read_only_fields = fields

    def get_sizes(self, obj: Product):
        return sorted(
            [
                TradeOfferSizeSerializer(instance=size, many=False, context=self.context).data
                for size in obj.sizes  # noqa
            ],
            key=lambda offer: offer["size"].get("translations", {}).get("ru", {}).get("size", "-"),
        )

    def get_exists_in_favorites(self, obj: Product):
        return obj.id in (
            self.context["request"].session.get("favorites")
            if self.context["request"].session.get("favorites")
            else []
        )

    def get_suggested_products(self, obj: Product):
        # если в связях нету активных продуктов "Вам может понравиться"
        # нужно выводить 8 радномных продуктов из категорий просматриваемого
        qs = (
            Product.objects.catalog_list_qs(
                custom_query=Q(Q(category__in=obj.category.filter(is_active=True)) & ~Q(pk=obj.pk))
            ).order_by("?")[:8]
            if not bool(
                len(
                    Product.objects.catalog_list_qs(
                        custom_query=Q(id__in=obj.suggested_products.all().values_list("id", flat=True))
                    )
                )
            )
            else Product.objects.catalog_list_qs(
                custom_query=Q(id__in=obj.suggested_products.all().values_list("id", flat=True))
            )[:8]
        )
        return ProductListSerializer(
            instance=qs,
            many=True,
            context=self.context,
        ).data

