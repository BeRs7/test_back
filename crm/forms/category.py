from django import forms

from catalog.models import Category
from utils.forms import BaseTranslatedModelForm


class CategoryUpdateForm(BaseTranslatedModelForm):
    widgets = {
        "name": forms.CharField(max_length=200, label="Название", required=False),
    }

    class Meta:
        model = Category
        fields = ("slug", "is_active", "on_main", "on_transactions", "order", "cover", "parent", "display_in_menu")
        multiple_languages_fields = ("name",)
        exclude = multiple_languages_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
