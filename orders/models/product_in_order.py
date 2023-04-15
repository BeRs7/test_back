from django.db import models

from catalog.models import Size, Color
from catalog.models.product import Product

___all__ = ("ProductInOrder",)

from orders.models.order import Order


class ProductInOrder(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Товар", related_name="product_in_orders"
    )
    cost = models.PositiveIntegerField("Цена", default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ", related_name="order_products")
    size = models.ForeignKey(Size, verbose_name="Размер", on_delete=models.SET_DEFAULT, null=True, default=None)
    color = models.ForeignKey(Color, verbose_name="Цвет", on_delete=models.SET_DEFAULT, null=True, default=None)
    quantity = models.PositiveIntegerField("Количество", default=1)

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"

    def __str__(self):
        return f"Товар в заказе #{self.order.id}"
