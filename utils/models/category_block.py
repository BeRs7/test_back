from django.db import models
from parler.models import TranslatableModel, TranslatedFields

from catalog.models import Category
from utils.choices import CategoryBlockLocation


class CategoryBlock(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(verbose_name="Заголовок", max_length=1023),
        description=models.CharField(verbose_name="Описание", max_length=1023),
    )
    slug = models.SlugField(verbose_name="Слаг", max_length=1023)
    order = models.PositiveIntegerField(verbose_name="Порядок", default=1)
    category = models.ManyToManyField(Category, verbose_name="Категория", related_name="category_blocks", blank=True)

    location = models.CharField(
        verbose_name="Расположение",
        choices=CategoryBlockLocation.CHOICES,
        default=CategoryBlockLocation.MAIN_PAGE,
        max_length=255,
    )

    class Meta:
        verbose_name = "Блок с категориями"
        verbose_name_plural = "Блок с категориями"
        ordering = ("order",)
