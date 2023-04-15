from pathlib import Path

from django.db import models
from parler.models import TranslatableModel, TranslatedFields, TranslationDoesNotExist
from solo.models import SingletonModel
from sorl.thumbnail import get_thumbnail
from ckeditor_uploader.fields import RichTextUploadingField

from utils.managers import BannerQuerySet


def get_upload_path(instance, filename):
    return Path(f"banners/{instance.id}/files/{filename}")


class AbstractBanner(models.Model):
    # info
    name = models.CharField("Название баннера", max_length=255, blank=True)
    link = models.CharField("Ссылка с баннера", max_length=2000, blank=True)
    order = models.PositiveIntegerField("Позиция", default=1)
    is_active = models.BooleanField("Активный", default=False)
    # images
    desktop_image = models.FileField("Изображение для десктопа", upload_to=get_upload_path, blank=True)
    mobile_image = models.FileField("Изображение для мобильных", upload_to=get_upload_path, blank=True)

    objects = BannerQuerySet.as_manager()

    @property
    def get_cropped_image_big(self):
        return get_thumbnail(self.desktop_image.file, "1920", crop="center").url if self.desktop_image else None

    @property
    def get_cropped_image_small(self):
        return get_thumbnail(self.mobile_image.file, "425", crop="center").url if self.mobile_image else None

    def change_status(self):
        self.is_active = not self.is_active
        self.save(update_fields=("is_active",))

    class Meta:
        abstract = True


class AbstractBannerSingleton(SingletonModel):
    # info
    name = models.CharField("Название баннера", max_length=255, blank=True)
    link = models.CharField("Ссылка с баннера", max_length=2000, blank=True)
    order = models.PositiveIntegerField("Позиция", default=1)
    is_active = models.BooleanField("Активный", default=False)
    # images
    desktop_image = models.FileField("Изображение для десктопа", upload_to=get_upload_path, blank=True)
    mobile_image = models.FileField("Изображение для мобильных", upload_to=get_upload_path, blank=True)

    objects = BannerQuerySet.as_manager()

    @property
    def get_cropped_image_big(self):
        return get_thumbnail(self.desktop_image.file, "1920", crop="center").url if self.desktop_image else None

    @property
    def get_cropped_image_crm(self):
        return get_thumbnail(self.desktop_image.file, "80x100", crop="center").url if self.desktop_image else None

    @property
    def get_cropped_image_small(self):
        return get_thumbnail(self.mobile_image.file, "425", crop="center").url if self.mobile_image else None

    def change_status(self):
        self.is_active = not self.is_active
        self.save(update_fields=("is_active",))

    class Meta:
        abstract = True


class MainBanner(AbstractBanner, TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField("Заголовок баннера", max_length=500, blank=True, null=True),
        button_text=models.CharField("Текст кнопки баннера", max_length=200, blank=True, null=True),
        subtitle=RichTextUploadingField("Подзаголовок баннера", max_length=500, blank=True),
    )

    class Meta:
        verbose_name = "Главный баннер"
        verbose_name_plural = "Главные баннеры"
        ordering = ("order",)

    def __str__(self):
        return f"{self.name} - Главный баннер"


class SecondBanner(AbstractBannerSingleton, TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField("Заголовок баннера", max_length=500, blank=True, null=True),
        subtitle=models.CharField("Подзаголовок баннера", max_length=500, blank=True),
    )

    class Meta:
        verbose_name = "Второй баннер"
        verbose_name_plural = "Вторые баннеры"
        ordering = ("order",)

    def __str__(self):
        try:
            return f"{self.name} - Второй баннер"
        except TranslationDoesNotExist:
            return 'Без названия - Второй баннер'


class Banner404(AbstractBannerSingleton, TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField("Заголовок баннера", max_length=500, blank=True, null=True),
        subtitle=models.CharField("Подзаголовок баннера", max_length=500, blank=True),
        button_left_text=models.CharField("Текст левой кнопки", max_length=500, blank=True),
        button_right_text=models.CharField("Текст правой кнопки", max_length=500, blank=True),
    )
    order = None
    link = None
    button_left_link = models.URLField("Ссылка левой кнопки")
    button_right_link = models.URLField("Ссылка правой кнопки")
    button_left_color = models.CharField("Цвет левой кнопки (HEX)", default="#000000", max_length=15)
    button_right_color = models.URLField("Цвет правой кнопки (HEX)", default="#000000", max_length=15)
    button_left_text_color = models.CharField("Цвет текста левой кнопки (HEX)", default="#ffffff", max_length=15)
    button_right_text_color = models.URLField("Цвет текста правой кнопки (HEX)", default="#ffffff", max_length=15)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "404 страница"
        verbose_name_plural = verbose_name
