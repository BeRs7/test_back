from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin


__all__ = ("FAQQuestionAdmin",)

from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm

from text_pages.models import FAQQuestion


class FAQQuestionAdminForm(TranslatableModelForm):
    class Meta:
        model = FAQQuestion
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["answer"].widget = CKEditorUploadingWidget()


@admin.register(FAQQuestion)
class FAQQuestionAdmin(TranslatableAdmin):
    search_fields = ["question", "id"]
    list_display = ["id", "question", "order", "is_active"]

    actions = ["turn_on", "turn_off"]

    def turn_on(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Вопросы включены")

    turn_on.short_description = "Включить выбранные вопросы"

    def turn_off(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Вопросы выключены")

    turn_off.short_description = "Выключить выбранные вопросы"
