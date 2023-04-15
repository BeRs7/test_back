from django.contrib import admin
from parler.admin import TranslatableAdmin
from solo.admin import SingletonModelAdmin

from utils.models import MainBanner, SecondBanner

__all__ = (
    "MainBannerAdmin",
    "SaleBannerAdmin",
)


@admin.register(MainBanner)
class MainBannerAdmin(TranslatableAdmin):
    fields = (
        "title",
        "subtitle",
        "button_text",
        "link",
        "desktop_image",
        "mobile_image",
        "is_active",
    )
    actions = ["disable_banner", "enable_banner"]

    def disable_banner(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Баннер выключен")

    disable_banner.short_description = "Выключить баннер"

    def enable_banner(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Баннер включен")

    enable_banner.short_description = "Включить баннер"


@admin.register(SecondBanner)
class SaleBannerAdmin(SingletonModelAdmin, TranslatableAdmin):
    list_display = ("name", "link", "is_active")
    actions = ["disable_banner", "enable_banner"]

    def disable_banner(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Баннер выключен")

    disable_banner.short_description = "Выключить баннер"

    def enable_banner(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Баннер включен")

    enable_banner.short_description = "Включить баннер"
