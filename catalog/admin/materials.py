from django.contrib import admin


__all__ = ("MaterialAdmin",)

from parler.admin import TranslatableAdmin

from catalog.models.specs import Material


@admin.register(Material)
class MaterialAdmin(TranslatableAdmin):
    search_fields = ["name"]
    fields = ["name", "display_on_main"]
