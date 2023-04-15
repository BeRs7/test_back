from django.db.models import CharField
from parler.models import TranslatableModel, TranslatedFields
from django.db import models


class ProductTag(TranslatableModel):
    translations = TranslatedFields(text=CharField(verbose_name="Текст тэга", max_length=100))
    slug = models.SlugField("slug", max_length=500, unique=True, default=None, null=True)
    is_active = models.BooleanField("Отображать", default=False)

    def __str__(self):
        return f"Тэг: {self.text}"

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
