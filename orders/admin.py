from django import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin

__all__ = (
    "OrderAdmin",
    "ProductInOrderInline",
)

from orders.choices import FittingTypeChoices
from orders.models import Order, ProductInOrder, RegistrationForFitting


class ProductInOrderInline(admin.StackedInline):
    model = ProductInOrder
    autocomplete_fields = ["product", "size", "color"]
    extra = 0

    def get_queryset(self, request):
        return ProductInOrder.objects.select_related("order", "product", "size", "color")


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    inlines = (ProductInOrderInline,)
    fields = [
        "status",
        "created_at",
        "locale",
        "paid_amount",
        "payment_date",
        "first_name",
        "last_name",
        "email",
        "phone",
        "country",
        "city",
        "zip_code",
        "comment",
        "payment_status",
        "cost",
        "delivery_cost",
        "discount_value",
        "summary_cost",
        "cart",
    ]
    readonly_fields = [
        "created_at",
        "locale",
        "paid_amount",
        "payment_date",
    ]
    list_display = [
        "id",
        "summary_cost",
        "discount_value",
        "payment_status",
        "created_at",
    ]

    def get_queryset(self, request):
        return Order.objects.all().select_related(
            "cart",
        )


@admin.register(RegistrationForFitting)
class RegistrationForFittingAdmin(ModelAdmin):
    readonly_fields = [
        "created",
        "external_id",
        "external_hash",
    ]
    service_type = forms.ChoiceField(choices=FittingTypeChoices.CHOICES)

