from utils.forms import StyledForm, BaseTranslatedModelForm
from django import forms

from utils.models import MainBanner, SecondBanner
from parler.forms import TranslatableModelForm
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CRMMainBannerUpdateForm(BaseTranslatedModelForm, StyledForm):
    title_ru = forms.CharField(label="Заголовок", required=False)
    title_en = forms.CharField(label="Заголовок (EN)", required=False)
    button_text_ru = forms.CharField(label="Текст кнопки", required=False)
    button_text_en = forms.CharField(label="Текст кнопки (EN)", required=False)
    subtitle_ru = forms.CharField(label="Подзаголовок", widget=CKEditorUploadingWidget(), required=False)
    subtitle_en = forms.CharField(label="Подзаголовок (EN)", widget=CKEditorUploadingWidget(), required=False)

    class Meta:
        model = MainBanner
        fields = [
            "link",
            "name",
            "desktop_image",
            "mobile_image",
            "link",
            "order",
            "is_active",
        ]
        multiple_languages_fields = (
            "title",
            "button_text",
            "subtitle",
        )
        exclude = multiple_languages_fields


class CRMSecondUpdateCreateForm(BaseTranslatedModelForm):
    style_after_init_hook = True
    widgets = {
        "title": forms.CharField(max_length=200, label="Заголовок", required=False),
        "subtitle": forms.CharField(label="Подзаголовок", widget=CKEditorUploadingWidget(), required=False),
    }

    class Meta:
        model = SecondBanner
        fields = [
            "link",
            "name",
            "desktop_image",
            "mobile_image",
            "is_active",
        ]
        multiple_languages_fields = (
            "title",
            "subtitle",
        )

