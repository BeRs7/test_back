from pathlib import Path

from django.db import models
from django.utils.translation import gettext_lazy as _

from parler.models import TranslatableModel, TranslatedFields
from ckeditor_uploader.fields import RichTextUploadingField
from sorl.thumbnail import get_thumbnail

from catalog.models.specs import Color, Size, Material
from catalog.models.category import Category
from catalog.models.managers import ProductQuerySet
from catalog.models.tags import ProductTag
from utils.files.models import FileAbstractModel


def autoincrement():
    return Product.objects.all().count() + 1


class Product(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Название"), max_length=200, null=True, blank=True),
        description=models.TextField("Описание", blank=True, null=True),
        # delivery=models.TextField("Варианты и сроки доставки", blank=True, null=True),
        # measurements=models.TextField("Обмеры", blank=True, null=True),
        model_measurements=models.TextField("Обмеры модели", blank=True, null=True),
        composition_and_care=RichTextUploadingField("Состав и уход", blank=True, null=True),
    )
    sku = models.CharField("Артикул", null=True, blank=True, max_length=32)
    video = models.FileField("Видео", null=True, blank=True)
    slug = models.SlugField("URL", max_length=500, unique=True)
    is_active = models.BooleanField("Включен", default=True)
    order = models.PositiveIntegerField("Сортировка", default=autoincrement)
    length = models.PositiveIntegerField("Длина", default=0)
    width = models.PositiveIntegerField("Ширина", default=0)
    weight = models.PositiveIntegerField("Вес в граммах", default=0)
    height = models.PositiveIntegerField("Высота", default=0)
    price = models.PositiveIntegerField("Розничная цена", default=0)
    price_with_sale = models.PositiveIntegerField("Розничная цена со скидкой", default=0)
    major_category = models.ForeignKey(
        Category,
        verbose_name="Главная категория",
        related_name="major_products",
        null=True,
        on_delete=models.SET_NULL
    )
    category = models.ManyToManyField(Category, verbose_name="Категория", related_name="category_products", blank=True)
    is_new = models.BooleanField("Новый", default=False)
    suggested_products = models.ManyToManyField(
        "self", verbose_name="Вам может понравиться", related_name="suggested_products", blank=True
    )
    color = models.ForeignKey(
        Color, verbose_name="Цвет", related_name="products", blank=True, null=True, on_delete=models.CASCADE
    )
    materials = models.ManyToManyField(
        Material,
        verbose_name="Материалы",
        related_name="products",
        blank=True,
    )
    tags = models.ManyToManyField(
        ProductTag,
        verbose_name="Тэги",
        related_name="products",
        blank=True,
    )
    seo_tags = models.ManyToManyField(
        ProductTag,
        verbose_name="SEO тэги",
        related_name="seo_products",
        blank=True,
    )
    colors = models.ManyToManyField(
        "self",
        verbose_name="Цвета",
        related_name="colors",
        blank=True,
    )
    total_look = models.ManyToManyField(
        "self",
        verbose_name="Дополни образ",
        related_name="look",
        blank=True,
    )
    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["order"]

    def __str__(self):
        try:
            if self.name:
                return self.name + ". " + self.color.name
            else:
                return self.id
        except Exception:
            return str(self.id)

    def get_weigth(self):
        """ Возвращает вес в граммах """
        if not bool(self.weight):  # вес не указан
            return 1000
        if self.weight < 5:  # вес указали в кг
            return self.weight * 1000
        return self.weight

    @property
    def get_current_price(self):
        return self.price_with_sale if self.price_with_sale else self.price

    @property
    def get_cropped_first_image(self):
        return get_thumbnail(self.images.first().file, "80x100", crop="center").url if self.images.exists() else None

    @property
    def get_first_image(self):
        return None if not self.images.exists() else self.images.first()

    @property
    def get_sizes(self):
        return [offer.size for offer in self.trade_offers.filter(is_active=True)]


def get_upload_path(instance, filename):
    return Path(f"products/{instance.product.id}/files/{filename}")


class ProductGallery(FileAbstractModel):
    product = models.ForeignKey(
        Product, verbose_name="Изображние товара", related_name="images", on_delete=models.CASCADE
    )
    file = models.FileField("Файл", upload_to=get_upload_path)
    order = models.PositiveIntegerField(verbose_name="Порядок", default=1)

    class Meta:
        verbose_name = "Галлерея товаров"
        verbose_name_plural = verbose_name
        ordering = ["order"]

    def get_file(self):
        return self.file.file if self.file else None
