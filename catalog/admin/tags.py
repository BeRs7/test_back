from django.contrib import admin


__all__ = ("ProductTagAdmin",)

from parler.admin import TranslatableAdmin

from catalog.models import ProductTag


@admin.register(ProductTag)
class ProductTagAdmin(TranslatableAdmin):
    search_fields = ["text", "slug"]
    fields = ["slug", "text", "is_active"]
