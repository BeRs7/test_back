from datetime import timedelta

from django.db import models
from django.db.models import Sum, F
from django.utils import timezone

from cart.models import Cart
from orders.choices.order import (
    StatusChoices,
    PaymentStatusChoices,
    PaymentTypeChoices,
    PickupTypeChoices,
)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время заказа")
    cart = models.ForeignKey(Cart, related_name="orders", null=True, blank=True, on_delete=models.SET_NULL)

    country = models.CharField("Страна", default="не указана", max_length=90, null=True)
    city = models.CharField("Город", default="не указан", max_length=189, null=True)
    zip_code = models.CharField("Индекс", default="не указан", max_length=18, null=True)
    street = models.CharField("Улица", max_length=150, null=True, default="не указана")
    house = models.CharField("Дом", max_length=150, null=True, default="не указан")
    house_building = models.CharField("Корпус", max_length=150, null=True, default="не указан")
    apartment = models.CharField("Квартира", max_length=150, null=True, default="не указана")
    weeding_date = models.DateField("Дата свадьбы", blank=True, null=True)
    bust_size = models.CharField("Обхват груди", blank=True, max_length=128)
    body_size = models.CharField("Обхват талии", blank=True, max_length=128)
    hip_size = models.CharField("Обхват бедер", blank=True, max_length=128)
    height = models.CharField("Рост", blank=True, max_length=128)
    first_name = models.CharField("Имя", max_length=150, null=True)
    last_name = models.CharField("Фамилия", max_length=150, null=True)
    email = models.EmailField("Email", max_length=100)
    phone = models.CharField("Телефон", max_length=17)
    comment = models.TextField("Комментарий", max_length=1000, blank=True)

    status = models.CharField(
        "Статус",
        choices=StatusChoices.CHOICES,
        default=StatusChoices.NEW,
        max_length=100,
    )
    payment_status = models.CharField(
        "Статус оплаты",
        choices=PaymentStatusChoices.CHOICES,
        default=PaymentStatusChoices.NOT_PAYED,
        max_length=100,
    )

    cost = models.PositiveIntegerField("Стоимость заказа", default=0)
    delivery_cost = models.PositiveIntegerField("Стоимость доставки", default=0)
    discount_value = models.PositiveIntegerField("Скидка руб", default=0)
    summary_cost = models.PositiveIntegerField("Общая стоимость", default=0)
    locale = models.CharField("Локализация", default="ru", max_length=20)
    paid_amount = models.CharField("Сумма оплаты", null=True, blank=True, max_length=20)
    paid_currency = models.CharField("Валюта оплаты", null=True, blank=True, max_length=10)
    payment_date = models.DateTimeField("Дата и время оплаты", null=True, blank=True)
    weight = models.PositiveIntegerField("Вес посылки", default=0)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ #{self.pk}"

    def get_total_count(self):
        return sum(product.quantity for product in self.order_products.all())

    def get_total_price(self):
        return sum(item.cost * item.quantity for item in self.order_products.all())

    @property
    def can_be_paid(self):
        return self.payment_status != PaymentStatusChoices.PAYED
        # return bool(
        #     (self.created_at + timedelta(hours=1)) > timezone.now()  # ссылка на оплату заказа живёт час
        #     and self.payment_url
        #     and self.payment_status != PaymentStatusChoices.PAYED
        # )

    @property
    def get_total_weight(self):
        return (
            self.order_products.aggregate(products_weight=Sum(F("product__weight") * F("quantity"))).get(
                "products_weight"
            )
            or 1000
        )
