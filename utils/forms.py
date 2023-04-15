from copy import deepcopy

from django import forms
from django.conf import settings
from django.db import transaction
from django.forms import widgets
from parler.forms import TranslatableModelForm
from django_select2.forms import ModelSelect2MultipleWidget

from utils.models import TempFile


class StyledForm(forms.Form):
    style_after_init_hook = False

    def style_fields(self, field):
        if field not in self.styled_fields:
            if not isinstance(self.fields[field].widget, ModelSelect2MultipleWidget):
                self.fields[field].widget.attrs.update({"class": f"form-control jsfield-{field}"})
            if isinstance(self.fields[field].widget, widgets.CheckboxInput):
                self.fields[field].widget.attrs["class"] = f"jsfield-{field} form-check-input"

            if isinstance(self.fields[field].widget, widgets.DateInput):
                self.fields[field].widget.attrs["class"] += " js-date-input"

            if isinstance(self.fields[field].widget, widgets.DateTimeInput):
                self.fields[field].widget.attrs["class"] += " js-datetime-input"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.styled_fields = []
        for field in self.fields:
            self.style_fields(field)
        try:
            self.post_init_hook()
        except Exception:
            pass
        for field in self.errors:
            if field != "__all__":
                if "class" in self.fields[field].widget.attrs:
                    self.fields[field].widget.attrs["class"] += " is-invalid"
                else:
                    self.fields[field].widget.attrs.update({"class": "is-invalid"})
                self.fields[field].errors = self.errors[field]


class StyledModelForm(TranslatableModelForm, StyledForm):
    pass


class TempFileForm(forms.ModelForm):
    class Meta:
        model = TempFile
        fields = "__all__"


class BaseTranslatedModelForm(StyledModelForm):
    def post_init_hook(self):
        self.instance.set_current_language("ru")
        for lang_code, lang_name in settings.LANGUAGES:
            for field in self.Meta.multiple_languages_fields:
                self.instance.set_current_language(lang_code)
                self.fields[f"{field}_" + lang_code] = deepcopy(self.widgets[field])
                if "class" in self.fields[f"{field}_" + lang_code].widget.attrs:
                    self.fields[f"{field}_" + lang_code].widget.attrs["class"] += f"form-control jsfield-{field}"
                else:
                    self.fields[f"{field}_" + lang_code].widget.attrs.update(
                        {"class": f"form-control jsfield-{field}"}
                    )

                if self.instance:
                    self.initial.setdefault(f"{field}_" + lang_code, getattr(self.instance, field, ""))
        self.instance.set_current_language("ru")

    @transaction.atomic
    def save(self, commit=True):
        instance = super().save(commit)
        self._save_m2m()
        for lang_code, lang_name in settings.LANGUAGES:
            instance.set_current_language(lang_code)
            for field in self.Meta.multiple_languages_fields:
                setattr(instance, field, self.cleaned_data[f"{field}_" + lang_code])
            instance.save()
        return instance

    @property
    def multiple_languages_fields(self):
        raise NotImplementedError

    @property
    def widgets(self):
        raise NotImplementedError
