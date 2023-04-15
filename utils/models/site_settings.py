from django.db import models
from parler.models import TranslatedFields, TranslatableModel
from solo.models import SingletonModel


class SiteSettings(SingletonModel, TranslatableModel):
    translations = TranslatedFields(
        header_offer=models.CharField("Предложение в шапке сайта", max_length=500, blank=True)
    )
    yandex_market_link = models.CharField("Ссылка на Yandex Market", max_length=500, blank=True)
    vk_link = models.CharField("Ссылка на VK", max_length=500, blank=True)
    instagram_link = models.CharField("Ссылка на Instagram", max_length=500, blank=True)
    site_phone = models.CharField("Телефон на сайте", max_length=500, blank=True)
    site_email = models.CharField("Email на сайте", max_length=500, blank=True)
    ceo_email_for_contacts = models.CharField("Email для обращений к руководителю", blank=True, max_length=500)

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "Настройки сайта"