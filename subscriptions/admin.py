from django.contrib import admin
from parler.admin import TranslatableAdmin

from subscriptions.models import Subscription

__all__ = ("SubscriptionAdmin",)


@admin.register(Subscription)
class SubscriptionAdmin(TranslatableAdmin):
    search_fields = [
        "email",
        "created_at",
        "is_active",
    ]
    list_display = [
        "email",
        "created_at",
        "is_active",
    ]
    readonly_fields = ["created_at"]
