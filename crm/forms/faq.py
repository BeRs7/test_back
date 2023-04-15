from ckeditor_uploader.widgets import CKEditorUploadingWidget

from text_pages.models import FAQQuestion
from utils.forms import BaseTranslatedModelForm
from django import forms


class CRMFAQQuestionCreationForm(BaseTranslatedModelForm):
    style_after_init_hook = True
    widgets = {
        "question": forms.CharField(label="Заголовок", required=False),
        "answer": forms.CharField(label="Текст (RU)", widget=CKEditorUploadingWidget(), required=False),
        "order": forms.IntegerField(label="Позиция", required=False),
    }

    class Meta:
        model = FAQQuestion
        fields = [
            "is_active",
            "order",
            "question",
            "answer",
        ]
        multiple_languages_fields = (
            "question",
            "answer",
        )
        exclude = multiple_languages_fields
