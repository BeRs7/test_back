from django.db.models import Q, Case, When
from django_filters import rest_framework as filters
from catalog.models import Product
from utils.filters import NumberInFilter, CharInFilter


class CatalogFilter(filters.FilterSet):

    # example: ?price_min=1000&price_max=2000
    price = filters.RangeFilter(
        label="Фильтр по цене",
    )
    search = filters.CharFilter(
        method="filter_search",
        label="Поиск",
    )
    category = filters.CharFilter(
        method="filter_category",
        label="Категория",
    )
    size = filters.CharFilter(
        method="filter_size",
        label="Размер",
    )
    color = filters.CharFilter(
        method="filter_color",
        label="Цвет",
    )
    tag = filters.CharFilter(
        method="filter_tags",
        label="Тэг",
    )
    materials = CharInFilter(
        method="filter_materials",
        label="Материалы",
    )
    ordering = filters.CharFilter(
        method="ordering_filter",
        label="Сортировка по цене (low-cost/high-cost)",
    )
    sale = filters.BooleanFilter(
        method="sale_filter",
        label="Фильтр 'по скидке'",
    )
    new = filters.BooleanFilter(
        method="new_filter",
        label="Фильтр 'новое'",
    )
    searching_fields = ("translations__name",)

    class Meta:
        model = Product
        distinct = True
        fields = ("search",)

    @staticmethod
    def filter_search(queryset, _, value):
        if value:
            q = Q()
            q |= Q(translations__name__icontains=value)
            q |= Q(translations__description__icontains=value)
            q |= Q(translations__composition_and_care__icontains=value)
            q |= Q(sku__icontains=value)
            return queryset.filter(q)
        return queryset

    def filter_category(self, queryset, _, value):
        if value:
            q = Q()
            q |= Q(category__slug__in=self.request.query_params.getlist("category"))
            q |= Q(category__parent__slug__in=self.request.query_params.getlist("category"))
            return queryset.filter(q)
        return queryset

    def filter_size(self, queryset, _, value):
        if value:
            q = Q()
            q |= Q(trade_offers__size__translations__in=self.request.query_params.getlist("size"))
            return queryset.filter(q)
        return queryset

    def filter_color(self, queryset, _, value):
        if value:
            q = Q()
            q |= Q(color__translations__name__in=self.request.query_params.getlist("color"))
            return queryset.filter(q)
        return queryset

    def filter_tags(self, queryset, _, value):
        if value:
            return queryset.filter(tags__slug__in=self.request.query_params.getlist("tag"))
        return queryset

    def filter_materials(self, queryset, _, value):
        if value:
            return queryset.filter(materials__name__in=self.request.query_params.getlist("materials"))
        return queryset

    def ordering_filter(self, queryset, _, value):
        if not value:
            return queryset

        if value == "high-cost":
            order_query = Case(  # сортируем кверисет по ценам - проблема была в том, что сортировка по одному полю,
                *[  # (price/price_with_sale) некорректна
                    When(pk=product.pk, then=pos)
                    for pos, product in enumerate(
                        sorted(queryset, reverse=True, key=lambda product: product.get_current_price)
                    )
                ]
            )
            return queryset.order_by(order_query)
        elif value == "low-cost":
            order_query = Case(  # сортируем кверисет по ценам - проблема была в том, что сортировка по одному полю,
                *[  # (price/price_with_sale) некорректна
                    When(pk=product.pk, then=pos)
                    for pos, product in enumerate(sorted(queryset, key=lambda product: product.get_current_price))
                ]
            )
            return queryset.order_by(order_query)
        elif value == "new":
            return queryset.order_by("-id")

        return queryset

    @staticmethod
    def sale_filter(queryset, _, value):
        if value:
            return queryset.filter(price_with_sale__gt=0)
        return queryset

    @staticmethod
    def new_filter(queryset, _, value):
        if value:
            return queryset.filter(is_new=True)
        return queryset
