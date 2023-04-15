from django.db import models


class Subscription(models.Model):
    email = models.EmailField(max_length=254, verbose_name="Email адрес", unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_active = models.BooleanField("Подписка активна", default=False)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
