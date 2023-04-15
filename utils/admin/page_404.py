from django.contrib import admin
from parler.admin import TranslatableAdmin
from solo.admin import SingletonModelAdmin

from utils.models import Banner404


@admin.register(Banner404)
class Page404Admin(TranslatableAdmin, SingletonModelAdmin):
    exclude = (
        "button_left_color",
        "button_right_color",
        "button_left_text_color",
        "button_right_text_color",
        "button_left_text",
        "button_right_text",
    )
