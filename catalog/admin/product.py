from django.contrib import admin
from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from catalog.models import Category, Product, ProductGallery, ProductTag

__all__ = ("ImageAdminInline", "ProductAdmin")


class ImageAdminInline(admin.TabularInline):
    model = ProductGallery
    fields = ("file", "order", "size_mb")
    readonly_fields = ("size_mb",)

    def get_queryset(self, request):
        return ProductGallery.objects.select_related("product").prefetch_related("product__translations")


class ProductAdminForm(TranslatableModelForm):
    class Meta:
        model = Product
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tags_qs = ProductTag.objects.filter(is_active=True).prefetch_related("translations")
        self.fields["category"].queryset = Category.objects.prefetch_related("translations")
        self.fields["tags"].queryset = tags_qs
        self.fields["seo_tags"].queryset = tags_qs
        self.fields["composition_and_care"].widget = CKEditorUploadingWidget()


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ["id", "order", "name", "price", "price_with_sale", "is_active"]
    search_fields = ["id", "translations__name", "slug"]
    list_filter = ["is_active", "category",  "color"]
    autocomplete_fields = ["category", "major_category", "tags", "seo_tags", "materials"]
    inlines = [ImageAdminInline]
    form = ProductAdminForm
    actions = ["turn_on", "turn_off"]

    fieldsets = (
        (
            "Главное",
            {
                "classes": ("collapse",),
                "fields": (
                    "name",
                    "sku",
                    "slug",
                    "is_active",
                    "category",
                    "major_category",
                    "color",
                    "description",
                    "model_measurements",
                    "composition_and_care",
                    "weight",
                ),
            },
        ),
        (
            "Общее",
            {
                "classes": ("collapse",),
                "fields": (
                    "is_new",
                    "materials",
                    "tags",
                    "seo_tags",
                    "price",
                    "price_with_sale",
                    "order",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        return Product.objects.all()

    def turn_on(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Продукты включены")

    turn_on.short_description = "Включить выбранные продукты"

    def turn_off(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Продукты выключены")

    turn_off.short_description = "Выключить выбранные продукты"
