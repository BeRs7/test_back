from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin


__all__ = ("TextPageAdmin",)

from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm

from text_pages.models import TextPage


class TextPageAdminForm(TranslatableModelForm):
    class Meta:
        model = TextPage
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget = CKEditorUploadingWidget()


@admin.register(TextPage)
class TextPageAdmin(TranslatableAdmin):
    search_fields = ["slug", "translations__title"]
    list_display = ["slug", "title"]
