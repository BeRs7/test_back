from django.contrib import admin

from cart.models import Cart, TradeOfferInCart

__all__ = ("CartAdmin",)


class TradeOfferInCartInline(admin.TabularInline):
    model = TradeOfferInCart
    autocomplete_fields = ("trade_offer",)
    fields = ("trade_offer", "quantity")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "status",
        "count_cart_products",
        "created_at",
        "last_activity",
        "username",
    )
    list_filter = ("created_at", "last_activity", "status")
    inlines = (TradeOfferInCartInline,)
    search_fields = ("username",)
    readonly_fields = (
        "created_at",
        "last_activity",
    )
    fields = (
        "username",
        "status",
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related(
                "products__trade_offer__product",
                "products__trade_offer__product__translations",
                "products__trade_offer__product__size",
                "products__trade_offer__product__size__translations",
            )
        )
