from pathlib import Path
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.db import models
from parler.models import TranslatedFields, TranslatableModel
from sorl.thumbnail import get_thumbnail

from catalog.managers import CategoryManager


def get_upload_path(instance, filename):
    return Path(f"categories/{instance.id}/files/{filename}")


class Category(MPTTModel, TranslatableModel):
    slug = models.SlugField("SLUG", max_length=500, unique=True)
    order = models.PositiveIntegerField("Сортировка", default=0)
    cover = models.FileField("Обложка категории", upload_to=get_upload_path, null=True, blank=True, default=None)
    cover_title = models.CharField("Заголовок на обложке", null=True, blank=True, max_length=128)
    cover_description = models.CharField("Описание на обложке", null=True, blank=True, max_length=128)
    translations = TranslatedFields(name=models.CharField("Название", max_length=500, null=True, blank=True))
    parent = TreeForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Родительская категория",
    )
    is_active = models.BooleanField("Категория активна", default=False)
    on_main = models.BooleanField("Выводить на главной", default=False)
    display_in_menu = models.BooleanField("Выводить в меню", default=False)
    on_transactions = models.BooleanField("Выводить на транзакционных страницах", default=False)
    objects = CategoryManager()

    class Meta:
        ordering = ("order",)
        verbose_name = "Категория"
        verbose_name_plural = "Справочник категорий"

    def __str__(self):
        try:
            if not self.parent:
                return f"Категория: {self.name}"
            else:
                return f"Категория: {self.name} | {self.parent.name}"
        except Exception:
            return f"Категория №{self.id}"

    @property
    def get_cropped_main_image(self):
        return get_thumbnail(self.cover, "80x100", crop="center").url if self.cover else None

    def change_is_active(self):
        self.is_active = not self.is_active
        self.save(update_fields=("is_active",))
