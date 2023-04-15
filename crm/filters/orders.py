from django.db.models import Q
from django.forms import CheckboxInput, DateInput
from django_filters import DateFilter, BooleanFilter

from orders.choices.order import StatusChoices
from orders.models import Order
from utils.filters import BaseFilter


class CRMOrdersFilter(BaseFilter):
    date_start = DateFilter(
        method="filter_date_start", widget=DateInput(attrs={"class": "form-control", "placeholder": "01.10.21"})
    )
    date_end = DateFilter(
        method="filter_date_end", widget=DateInput(attrs={"class": "form-control", "placeholder": "15.03.22"})
    )
    new = BooleanFilter(method="filter_new", widget=CheckboxInput(attrs={"class": "form-check-input"}))
    payed = BooleanFilter(method="filter_payed", widget=CheckboxInput(attrs={"class": "form-check-input"}))
    canceled = BooleanFilter(method="filter_canceled", widget=CheckboxInput(attrs={"class": "form-check-input"}))

    searching_fields = (
        "id",
        "email",
        "phone",
        "status",
    )

    class Meta:
        model = Order
        fields = ["id", "email", "phone", "status"]

    def filter_date_start(self, qs, _, value):
        q = Q()
        if value:
            q &= Q(created_at__gte=value)
        return qs.filter(q)

    def filter_date_end(self, qs, _, value):
        q = Q()
        if value:
            q &= Q(created_at__lte=value)
        return qs.filter(q)

    def filter_new(self, qs, _, value):
        q = Q()
        if value:
            q &= Q(status=StatusChoices.NEW)
        return qs.filter(q)

    def filter_canceled(self, qs, _, value):
        q = Q()
        if value:
            q &= Q(status=StatusChoices.CANCELED)
        return qs.filter(q)

    def filter_payed(self, qs, _, value):
        q = Q()
        if value:
            q &= Q(status=StatusChoices.PREPAYED)
        return qs.filter(q)
