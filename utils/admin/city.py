from django.contrib import admin

from utils.models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = [
        "ru_name",
        "en_name",
        "country",
        "iso",
    ]
    list_filter = ["country", "iso"]
    search_fields = list_display
    ordering = ["id"]
