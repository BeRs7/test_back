from django.db import models


class City(models.Model):
    ru_name = models.CharField("Название города RU", max_length=100)
    en_name = models.CharField("Название города EN", max_length=100)
    country = models.CharField("Страна", max_length=100, null=True)
    iso = models.CharField("ISO страны", max_length=10, null=True)
    zip_code = models.CharField("Индекс", max_length=30, null=True)

    def __str__(self):
        return self.ru_name

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "База городов"
