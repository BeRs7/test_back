from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField("E-mail", unique=True)
    phone_number = models.CharField("Номер телефона", max_length=30, blank=True, null=True)
    first_name = models.CharField("Имя пользователя", max_length=100, blank=True, null=True)
    last_name = models.CharField("Фамилия пользователя", max_length=100, blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return "Пользователь {}".format(self.email)

    def get_full_name(self):
        if self.first_name and self.last_name:
            full_name = super().get_full_name()
        else:
            full_name = self.email
        return full_name

    @property
    def is_can_access_crm(self) -> bool:
        return (self.is_staff or self.is_superuser) and self.is_active