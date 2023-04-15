from django.db import models
from django.db.models import QuerySet, Max

from catalog.models.product import Product
from catalog.models.specs import Size


class TradeOfferQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True).prefetch_related(
            "size", "size__translations"
        ).annotate(sort_field=Max("size__translations__size")).order_by("sort_field")


class TradeOffer(models.Model):
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.CASCADE, related_name="trade_offers")
    size = models.ForeignKey(Size, verbose_name="Размер", on_delete=models.CASCADE, related_name="size_trade_offers")
    amount = models.PositiveIntegerField(verbose_name="Количество", default=0)
    is_active = models.BooleanField("Активен", default=False)

    objects = TradeOfferQuerySet.as_manager()

    class Meta:
        verbose_name = "Торговое предложение"
        verbose_name_plural = "Торговые предложения"

    def __str__(self):
        try:
            return f"Товар {self.product.name}. Размер: {self.size}. {self.amount} шт."
        except Exception:
            return str(self.id)

    def get_is_active(self):
        return self.is_active and self.amount > 0 and self.product.is_active
