from django.contrib import admin, auth
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm

from users.models import User


class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    fieldsets = (
        (
            "Главная информация",
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Личная информация",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                )
            },
        ),
        ("Статус", {"fields": ("is_staff", "is_superuser", "is_active")}),
    )
    list_display = ("id", "email", "phone_number", "is_superuser", "is_active")
    ordering = ["id"]
    form = UserChangeForm


admin.site.register(User, UserAdmin)
admin.site.unregister(auth.models.Group)
