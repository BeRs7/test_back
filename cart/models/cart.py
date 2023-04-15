from typing import Optional

from django.db import models
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.http import HttpRequest
from django.utils import timezone

from cart.managers import CartQuerySet
from catalog.models import TradeOffer


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    last_activity = models.DateTimeField(verbose_name="Дата активности")
    username = models.CharField("Email", max_length=256, null=True, blank=True)
    status = models.CharField(
        "Статус",
        choices=(("not_completed", "Не закончена"), ("completed", "Перешло на оформление"), ("payed", "Оформлена")),
        default="not_completed",
        max_length=50,
    )
    objects = CartQuerySet.as_manager()

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        ordering = ["-last_activity"]

    def save(self, *args, **kwargs):
        self.update_last_activity()
        return super().save(*args, **kwargs)

    def update_last_activity(self):
        self.last_activity = timezone.now()

    def count_cart_products(self):
        return self.products.all().aggregate(products_count=Coalesce(Sum("quantity"), 0)).get("products_count")

    count_cart_products.short_description = "Количество продуктов в корзине"

    @staticmethod
    def get_cart_from_request(request: HttpRequest) -> "Cart":
        query = Q()
        cart = None

        cart_pk = request.session.get("cart", None)
        if type(cart_pk) != int:
            cart_pk = None

        if cart_pk:
            query |= Q(pk=cart_pk)

        if query:
            cart = Cart.objects.active().filter(query).first()

        if not cart or cart.status == "payed":
            cart = Cart.objects.create()
            request.session["cart"] = cart.pk

        return cart  # type: Cart

    def get_trade_offer_in_cart(self, trade_offer: TradeOffer) -> "TradeOfferInCart" or None:
        return self.products.filter(trade_offer=trade_offer).first()  # type: TradeOfferInCart or None

    def add_to_cart(self, trade_offer: TradeOffer, quantity: Optional[int] = 1) -> None:
        product_in_cart = self.get_trade_offer_in_cart(trade_offer)  # type: TradeOfferInCart or None
        if product_in_cart:
            product_in_cart.quantity += quantity
            product_in_cart.save(update_fields=("quantity",))
        else:
            TradeOfferInCart.objects.create(cart=self, trade_offer=trade_offer, quantity=quantity)

        self.update_last_activity()
        self.save(update_fields=("last_activity",))
        return

    def remove_from_cart(self, trade_offer: TradeOffer, quantity: Optional[int] = 1) -> None:
        product_in_cart = self.get_trade_offer_in_cart(trade_offer)  # type: TradeOfferInCart
        if product_in_cart:
            if product_in_cart.quantity <= quantity:
                product_in_cart.delete()
            else:
                product_in_cart.quantity -= quantity
                product_in_cart.save(update_fields=("quantity",))

        self.update_last_activity()
        self.save(update_fields=("last_activity",))
        return

    def get_cart_total_sum(self) -> int:
        return sum(
            [
                trade_offer_in_cart.trade_offer.product.get_current_price * trade_offer_in_cart.quantity
                for trade_offer_in_cart in self.products.all().prefetch_related("trade_offer", "trade_offer__product")
            ]
        )

    def get_cart_quantity_and_sum(self) -> dict:
        """
        Функция возвращает словарь с общим кол-вом продуктов в корзине и общей стоимостью корзины
        """
        qs = (
            self.products.all()
            .only("quantity")
            .aggregate(
                quantity=Coalesce(Sum("quantity"), 0),
            )
        )
        return {"quantity": qs.get("quantity"), "total_sum": self.get_cart_total_sum()}

    def get_weight_of_products(self) -> int:
        """
        Функция возвращает вес корзины в гр.
        """

        def convert_weight(weight):
            if weight == 0:
                return 1000
            elif weight < 5:  # если вес ввели в кг
                return weight * 1000
            else:
                return weight

        return sum(
            [
                convert_weight(product_in_cart.trade_offer.product.weight) * product_in_cart.quantity
                for product_in_cart in self.products.all()
                .prefetch_related("trade_offer", "trade_offer__product")  # type: TradeOfferInCart
            ]
        )


class TradeOfferInCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="products")
    trade_offer = models.ForeignKey(
        TradeOffer, on_delete=models.CASCADE, related_name="carts", verbose_name="Торговое предложение"
    )
    quantity = models.PositiveIntegerField("Количество в корзине", default=0)

    class Meta:
        ordering = ("id",)
        verbose_name = "Продукт в заказе"
        verbose_name_plural = "Продукты в заказах"
