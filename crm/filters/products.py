import ast

import django_filters as filters
from django.db.models import Q
from django.forms import CheckboxInput, NumberInput, CheckboxSelectMultiple

from catalog.models import Product, Category, Size
from utils.filters import BaseFilter


class CRMProductFilter(BaseFilter):
    o = filters.OrderingFilter(fields=(("price", "price"), ("order", "order")))
    is_active = filters.BooleanFilter(
        method="filter_is_active", widget=CheckboxInput(attrs={"class": "form-check-input"})
    )
    is_bestseller = filters.BooleanFilter(
        method="filter_is_bestseller", widget=CheckboxInput(attrs={"class": "form-check-input"})
    )

    price_start = filters.NumberFilter(
        method="filter_price_start", widget=NumberInput(attrs={"class": "form-control", "placeholder": "10500"})
    )
    price_end = filters.NumberFilter(
        method="filter_price_end", widget=NumberInput(attrs={"class": "form-control", "placeholder": "15000"})
    )

    is_soon = filters.BooleanFilter(method="filter_is_soon", widget=CheckboxInput(attrs={"class": "form-check-input"}))
    is_new = filters.BooleanFilter(method="filter_is_new", widget=CheckboxInput(attrs={"class": "form-check-input"}))

    size = filters.CharFilter(
        field_name="size__translations__size",
        method="filter_size",
    )

    category = filters.CharFilter(
        field_name="category__translations__name",
        method="filter_category",
    )
    searching_fields = ("id", "translations__name")

    class Meta:
        model = Product
        fields = [
            "id",
            "translations__name",
            "is_active",
            "is_bestseller",
            "is_soon",
            "is_new",
            "price_start",
            "price_end",
            "category",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields["size"].widget = CheckboxSelectMultiple(
            choices=Size.objects.values_list("translations__size", "translations__size"),
            attrs={"class": "form-check-input"},
        )
        self.form.fields["category"].widget = CheckboxSelectMultiple(
            choices=Category.objects.filter(translations__language_code="ru").values_list(
                "translations__name", "translations__name"
            ),
            attrs={"class": "form-check-input"},
        )

    def filter_is_active(self, qs, _, value):
        q = Q()
        if value:
            q &= Q(is_active=True)
        return qs.filter(q)

    def filter_is_bestseller(self, qs, _, value):
        q = Q()
        if value:
            q &= Q(is_bestseller=True)
        return qs.filter(q)

    def filter_is_soon(self, qs, _, value):
        q = Q()
        if value:
            q &= Q(is_soon=True)
        return qs.filter(q)

    def filter_is_new(self, qs, _, value):
        q = Q()
        if value:
            q &= Q(is_new=True)
        return qs.filter(q)

    def filter_price_start(self, qs, _, value):
        q = Q()
        if value:
            q &= Q(price__gte=value)
        return qs.filter(q)

    def filter_price_end(self, qs, _, value):
        q = Q()
        if value:
            q &= Q(price__lte=value)
        return qs.filter(q)

    def filter_size(self, qs, _, value):
        q = Q()
        value = ast.literal_eval(value)
        if value:
            q |= Q(size__translations__size__in=value)
        return qs.filter(q).distinct()

    def filter_category(self, qs, _, value):
        q = Q()
        value = ast.literal_eval(value)
        if value:
            q |= Q(category__translations__name__in=value)
        return qs.filter(q).distinct()
