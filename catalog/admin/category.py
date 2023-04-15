from django.contrib import admin
from django.forms import forms
from mptt.admin import MPTTModelAdmin
from mptt.forms import MPTTAdminForm
from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm

from catalog.models.category import Category

__all__ = ("CategoryAdmin",)


class CategoryAdminForm(MPTTAdminForm, TranslatableModelForm):
    cover = forms.FileField(required=False)

    class Meta:
        model = Category
        exclude = ()


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin, MPTTModelAdmin):
    form = CategoryAdminForm
    list_display = [
        "parent",
        "name",
        "order",
        "slug",
        "is_active",
        "on_main",
        "on_transactions",
    ]
    search_fields = ["translations__name", "slug"]
    actions = ["turn_on", "turn_off"]

    def turn_on(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Категории включены")

    turn_on.short_description = "Включить выбранные категории"

    def turn_off(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Категории выключены")

    turn_off.short_description = "Выключить выбранные категории"
