import django_filters as filters
from django.db.models import Q
from django.forms import CheckboxInput

from catalog.models import Category
from utils.filters import BaseFilter


class CRMCategoriesFilter(BaseFilter):
    searching_fields = ("id", "translations__name", "slug")

    o = filters.OrderingFilter(fields=(("price", "price"),))
    is_display_on_main = filters.BooleanFilter(
        method="filter_is_display_on_main", widget=CheckboxInput(attrs={"class": "form-check-input"})
    )
    is_active = filters.BooleanFilter(
        method="filter_is_active", widget=CheckboxInput(attrs={"class": "form-check-input"})
    )

    class Meta:
        model = Category
        fields = ["id", "translations__name", "slug", "is_display_on_main", "is_active"]

    def filter_is_display_on_main(self, qs, _, value):
        q = Q()
        if value:
            q &= Q(is_display_on_main=True)
        return qs.filter(q)

    def filter_is_active(self, qs, _, value):
        q = Q()
        if value:
            q &= Q(is_active=True)
        return qs.filter(q)
