from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime as dt

from loyalty.models import PromoCode
from django import forms

from utils.forms import StyledForm


class PromocodeUpdateForm(forms.ModelForm, StyledForm):
    date_start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    date_start_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    date_start = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={"readonly": "readonly"}))
    date_end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    date_end_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    date_end = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={"readonly": "readonly"}))
    min_sum_for_discount = forms.IntegerField(required=False)

    class Meta:
        model = PromoCode
        fields = "__all__"
        widgets = {}
        error_messages = {
            "discount_type": {
                "required": "Тип скидки - обязательное поле",
            },
            "name": {
                "required": "Код - обязательное поле",
            },
            "discount": {"required": "Значение скидки - обязательное поле"},
            "quantity": {"required": "Количество - обязательное поле"},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        to_tz = timezone.get_default_timezone()
        if self.instance.date_end:
            self.fields["date_end_time"].initial = self.instance.date_end.astimezone(to_tz).time()
            self.fields["date_end_date"].initial = self.instance.date_end.astimezone(to_tz).date().strftime("%Y-%m-%d")
        if self.instance.date_start:
            self.fields["date_start_time"].initial = self.instance.date_start.astimezone(to_tz).time()
            self.fields["date_start_date"].initial = (
                self.instance.date_start.astimezone(to_tz).date().strftime("%Y-%m-%d")
            )

    def clean(self):
        if not self.cleaned_data.get("date_start_date") or not self.cleaned_data.get("date_start_time"):
            self.add_error("date_start_date", "Укажите дату начала действий")
            self.add_error("date_start_time", "Укажите время начала дейтсвий")
            raise ValidationError({"date_start": "Укажите дату начала"})
        if not self.cleaned_data.get("date_end_date") or not self.cleaned_data.get("date_end_time"):
            self.add_error("date_end_date", "Укажите дату конца действий")
            self.add_error("date_end_time", "Укажите время конца дейтсвия")
            raise ValidationError({"date_end": "Укажите верную дату конца действия промокода"})
        self.cleaned_data["date_start"] = dt.datetime.combine(
            self.cleaned_data.pop("date_start_date"), self.cleaned_data.pop("date_start_time")
        )
        self.cleaned_data["date_end"] = dt.datetime.combine(
            self.cleaned_data.pop("date_end_date"), self.cleaned_data.pop("date_end_time")
        )
        super().clean()
        return self.cleaned_data
