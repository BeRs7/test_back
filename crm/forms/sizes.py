from utils.forms import BaseTranslatedModelForm
from catalog.models import Color, Size
from django import forms


class CRMSizesCreationForm(BaseTranslatedModelForm):
    style_after_init_hook = True
    widgets = {
        "size": forms.CharField(label="Название", required=False),
    }

    class Meta:
        model = Size
        fields = [
            "display_on_main",
        ]
        multiple_languages_fields = ("size",)
        exclude = multiple_languages_fields
