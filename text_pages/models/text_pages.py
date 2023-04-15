from pathlib import Path
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from parler.models import TranslatableModel, TranslatedFields


def get_upload_path(instance, filename):
    return Path(f"banners/{instance.id}/files/{filename}")


class TextPage(TranslatableModel):
    slug = models.SlugField("SLUG", max_length=500, unique=True)
    menu_position = models.CharField("Раздел в меню", choices=(("buyers", "Покупателям"), ("about", "О компании")), max_length=500, default="buyers")
    translations = TranslatedFields(
        title=models.CharField("Заголовок", max_length=150),
        content=RichTextUploadingField("Контент", blank=True, null=True),
        seo_title=models.CharField("SEO Заголовок", max_length=150, blank=True, null=True),
        seo_content=models.CharField("SEO Контент", max_length=150, blank=True, null=True),
    )
    # desktop_image = models.FileField("Изображение для десктопа", upload_to=get_upload_path, blank=True)
    # mobile_image = models.FileField("Изображение для мобильных", upload_to=get_upload_path, blank=True)
    is_active = models.BooleanField("Активна", default=False)
    show_in_footer = models.BooleanField("Отображать в футере", default=False)
    ordering = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Текстовая страница"
        verbose_name_plural = "Текстовые страницы"
        ordering = ("ordering",)

    def __str__(self):
        try:
            return self.title
        except Exception:
            return self.slug
