from utils.forms import BaseTranslatedModelForm
from catalog.models import Color
from django import forms


class CRMColorColorCreationForm(BaseTranslatedModelForm):
    style_after_init_hook = True
    widgets = {
        "name": forms.CharField(label="Название", required=False),
    }

    class Meta:
        model = Color
        fields = [
            "hex",
            "display_on_main",
        ]
        multiple_languages_fields = ("name",)
        exclude = multiple_languages_fields
