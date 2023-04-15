from django.db import models
from django.utils import timezone

from orders.choices.fittings import FittingTypeChoices


class RegistrationForFitting(models.Model):
    full_name = models.CharField("Имя и фамилия", max_length=256)
    phone = models.CharField("Телефон", max_length=17)
    email = models.EmailField("Email", max_length=100, null=True, blank=True)
    date_of_wedding = models.DateField("Дата свадьбы", null=True, blank=True)
    comment = models.CharField("Комментарий", max_length=1024, null=True, blank=True)
    created = models.DateTimeField("Дата создания", auto_now_add=True)
    time = models.DateTimeField("Время примерки")
    service_type = models.IntegerField("Тип примерки", choices=FittingTypeChoices.CHOICES)
    external_id = models.CharField("Внешний ид", null=True, blank=True, max_length=256)
    external_hash = models.CharField("Внешний hash", null=True, blank=True, max_length=256)

    class Meta:
        verbose_name = "Запись на примерку"
        verbose_name_plural = "Записи на примерку"
        ordering = ("time",)

    def __str__(self):
        return f"Запись на примерку #{self.pk} | {self.time.astimezone(timezone.get_default_timezone())}"  # noqa
