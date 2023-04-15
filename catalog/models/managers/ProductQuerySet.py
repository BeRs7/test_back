from typing import Optional

from django.db.models import Prefetch, Q
from parler.managers import TranslatableQuerySet


class ProductQuerySet(TranslatableQuerySet):
    def active(self):
        from catalog.models.tags import ProductTag
        from catalog.models.product import Product

        return (
            self.filter(
                major_category__isnull=False, is_active=True, color__isnull=False, images__isnull=False, price__gt=0
            )
            .distinct()
            .prefetch_related(
                "translations",
                "color",
                "images",
                Prefetch("tags", queryset=ProductTag.objects.filter(is_active=True)),
                Prefetch("seo_tags", queryset=ProductTag.objects.filter(is_active=True)),
                Prefetch("total_look", queryset=Product.objects.for_show()),
                "trade_offers",
                "trade_offers__product",
                "trade_offers__product__translations",
                "trade_offers__size",
                "trade_offers__size__translations",
                'category',
                'major_category',
                'category__translations',
                'major_category__translations',
            )
            .order_by("order")
        )

    def for_show(self):
        from catalog.models.tags import ProductTag

        return (
            self.filter(is_active=True, color__isnull=False, images__isnull=False, price__gt=0)
            .distinct()
            .prefetch_related(
                "translations",
                "color",
                "images",
                Prefetch("tags", queryset=ProductTag.objects.filter(is_active=True)),
                Prefetch("seo_tags", queryset=ProductTag.objects.filter(is_active=True)),
                'category',
                'major_category',
                'category__translations',
                'major_category__translations',
            )
            .order_by("order")
        )

    def catalog_list_qs(self, custom_query: Optional[Q] = None):
        from catalog.models.tags import ProductTag
        from catalog.models.product import Product
        from catalog.models import TradeOffer

        query = Q(
            is_active=True,
            color__isnull=False,
            images__isnull=False,
            price__gt=0,
        )
        if custom_query:
            query &= custom_query
        return (
            self.filter(query)
            .distinct()
            .prefetch_related(
                "translations",
                "color",
                "color__translations",
                "images",
                Prefetch("tags", queryset=ProductTag.objects.filter(is_active=True)),
                Prefetch("seo_tags", queryset=ProductTag.objects.filter(is_active=True)),
                Prefetch("total_look", queryset=Product.objects.for_show()),
                Prefetch("colors", queryset=Product.objects.for_show()),
                Prefetch("suggested_products", queryset=Product.objects.for_show()),
                Prefetch("trade_offers", queryset=TradeOffer.objects.active(), to_attr="sizes"),
                'category',
                'major_category',
                'category__translations',
                'major_category__translations',
            ).distinct()
        )
