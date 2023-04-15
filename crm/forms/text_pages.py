from ckeditor_uploader.widgets import CKEditorUploadingWidget

from text_pages.models import TextPage
from utils.forms import BaseTranslatedModelForm
from django import forms


class CRMTextPageCreationForm(BaseTranslatedModelForm):
    style_after_init_hook = True
    widgets = {
        "title": forms.CharField(label="Заголовок", required=False),
        "content": forms.CharField(label="Текст", widget=CKEditorUploadingWidget(), required=False),
        "seo_title": forms.CharField(label="SEO Заголовок", required=False),
        "seo_content": forms.CharField(label="SEO Контент", required=False),
        "ordering": forms.IntegerField(label="Позиция", required=False),
    }

    class Meta:
        model = TextPage
        fields = [
            "slug",
            "is_active",
            "show_in_footer",
            "ordering",
            "title",
            "content",
            "menu_position",
        ]
        multiple_languages_fields = (
            "title",
            "content",
            "seo_title",
            "seo_content",
        )
        exclude = multiple_languages_fields
