from django.contrib import admin


__all__ = ("SizeAdmin",)

from parler.admin import TranslatableAdmin

from catalog.models import Size


@admin.register(Size)
class SizeAdmin(TranslatableAdmin):
    search_fields = ["size"]
    list_display = ["size", "display_on_main"]
