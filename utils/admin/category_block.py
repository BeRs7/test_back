from django.contrib import admin
from parler.admin import TranslatableAdmin

from utils.models import CategoryBlock


@admin.register(CategoryBlock)
class CategoryBlockAdmin(TranslatableAdmin):
    list_filter = ("location", "category")
    list_display = ("location", "slug")
    autocomplete_fields = ["category"]
