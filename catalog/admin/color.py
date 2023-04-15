from django.contrib import admin


__all__ = ("ColorAdmin",)

from parler.admin import TranslatableAdmin

from catalog.models import Color


@admin.register(Color)
class ColorAdmin(TranslatableAdmin):
    search_fields = ["translations__name"]
    list_display = ["name", "display_on_main"]
    actions = ["turn_on", "turn_off"]

    def turn_on(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Цвета включены")

    turn_on.short_description = "Включить выбранные цвета"

    def turn_off(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Цвета выключены")

    turn_off.short_description = "Выключить выбранные цвета"
