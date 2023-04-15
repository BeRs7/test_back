from colorfield.fields import ColorField
from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class Size(TranslatableModel):
    translations = TranslatedFields(size=models.CharField("Размер", max_length=255))
    display_on_main = models.BooleanField("Отображать в фильтрах", default=False)

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"

    def __str__(self):
        try:
            if self.size:
                return f"Размер: {self.size}"
        except:
            return str(self.id)


class Color(TranslatableModel):
    translations = TranslatedFields(name=models.CharField("Название", max_length=500, null=True, blank=True))
    hex = ColorField("HEX код цвета", max_length=32, null=True, blank=True)
    display_on_main = models.BooleanField("Отображать в фильтрах", default=False)

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Справочник цветов"

    def __str__(self):
        try:
            if self.name:
                return self.name
        except:
            return str(self.id)


class Material(TranslatableModel):
    translations = TranslatedFields(name=models.CharField("Название", max_length=500, null=True, blank=True))
    display_on_main = models.BooleanField("Отображать в фильтрах", default=False)

    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Справочник материалов"

    def __str__(self):
        try:
            if self.name:
                return self.name
        except:
            return str(self.id)
