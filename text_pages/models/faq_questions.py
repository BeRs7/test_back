from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class FAQQuestion(TranslatableModel):
    translations = TranslatedFields(
        question=models.CharField("Вопрос", max_length=150),
        answer=RichTextUploadingField("Ответ", blank=True, null=True),
    )
    order = models.PositiveIntegerField("Позиция", default=5)
    is_active = models.BooleanField("Активна", default=False)

    class Meta:
        verbose_name = "Вопросс FAQ"
        verbose_name_plural = "Вопросы FAQ"
        ordering = ("order",)

    def __str__(self):
        try:
            return self.question
        except Exception:
            return str("Вопрос FAQ №{}".format(self.id))
