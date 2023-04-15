import django_filters as filters
import django_filters.rest_framework as django_filters
from django.db.models import Q


class BaseFilter(filters.FilterSet):
    search_field_placeholder = "Начните вводить..."

    search = filters.CharFilter(method="filter_search")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields["search"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": self.search_field_placeholder,
            }
        )

    def filter_search(self, qs, _, value):
        if value:
            q_objects = Q()
            for field in self.searching_fields:
                q_objects |= Q(**{f"{field}__icontains": value})
            qs = qs.filter(q_objects)
        return qs.distinct()


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass
