from django import forms

from utils.models.currency import CurrencySettings
from utils.forms import StyledForm


class SettingsUpdateForm(forms.ModelForm, StyledForm):
    widgets = {
        "dollar_rate": forms.FloatField(label="Курс доллара в рублях", required=True),
        "euro_rate": forms.FloatField(label="Курс доллара в рублях", required=True),
    }

    class Meta:
        model = CurrencySettings
        fields = (
            "dollar_rate",
            "dollar_allow",
            "euro_rate",
            "euro_allow",
        )
