from django.forms import ModelForm

from catalog.models import Size, TradeOffer
from django.contrib import admin


class TradeOfferAdminForm(ModelForm):
    class Meta:
        model = TradeOffer
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["size"].queryset = Size.objects.all()


class TradeOfferAdminInline(admin.TabularInline):
    model = TradeOffer
    form = TradeOfferAdminForm

    def get_queryset(self, request):
        return TradeOffer.objects.all()


@admin.register(TradeOffer)
class TradeOfferAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "size", "amount", "is_active"]
    search_fields = ["product__translations__name"]
    autocomplete_fields = [
        "product",
        "size",
    ]
    fields = [
        "product",
        "size",
        "amount",
        "is_active",
    ]
    actions = ["turn_on", "turn_off"]

    def turn_on(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Торговые предложения включены")

    turn_on.short_description = "Включить выбранные торговые предложения"

    def turn_off(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Торговые предложения выключены")

    turn_off.short_description = "Выключить выбранные торговые предложения"
