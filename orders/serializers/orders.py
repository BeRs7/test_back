from django.db import transaction
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from cart.models import Cart, TradeOfferInCart
from catalog.models import Product
from orders.models import Order, ProductInOrder
from orders.tasks.emails import send_created_order_information
from rest_framework import serializers


# TODO: сделать для фронта view владиации промокода до отправки создания заказа
class OrderCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = Order
        fields = [
            "country",
            "city",
            "zip_code",
            "street",
            "house",
            "house_building",
            "apartment",
            "first_name",
            "last_name",
            "email",
            "phone",
            "comment",
            "weeding_date",
            "bust_size",
            "body_size",
            "hip_size",
            "height",
        ]

    def validate(self, attrs):
        # если в дб не найден промокод, закидываем его в поле maxma_promocode для последующей валидации
        attrs = super(OrderCreateSerializer, self).validate(attrs)
        request = self.context["request"]
        cart = Cart.get_cart_from_request(request)  # type: Cart
        cart.status = "completed"
        cart.save(update_fields=["status"])
        attrs["cart"] = cart

        for product_in_cart in cart.products.all().prefetch_related("trade_offer", "trade_offer__product"):
            if product_in_cart.trade_offer.amount < product_in_cart.quantity:
                raise serializers.ValidationError(
                    {
                        "product_{}".format(product_in_cart.trade_offer.product.id):
                            _("Максимальное количество продукта: {}").format(product_in_cart.trade_offer.amount)
                    }
                )
            if product_in_cart.trade_offer.product.is_active is False:
                raise serializers.ValidationError(
                    {
                        "product_{}".format(product_in_cart.trade_offer.product.id):
                            _("Продукт снят с продажи").format(product_in_cart.trade_offer.product.amount)
                    }
                )
            if product_in_cart.trade_offer.product.price == 0:
                raise serializers.ValidationError(
                    {
                        "product_{}".format(product_in_cart.trade_offer.product.id):
                            _("Продукт некорректно заполнен").format(product_in_cart.trade_offer.product.amount)
                    }
                )

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        cart = validated_data["cart"]  # type: Cart
        cart.username = validated_data["email"]
        cart.save(update_fields=("username",))

        order = Order.objects.create(**validated_data)

        request = self.context["request"]
        if "/en/" in request.META.get("HTTP_REFERER", request.path):
            validated_data["locale"] = "en"
        else:
            validated_data["locale"] = "ru"

        products = cart.products.all()  # type: QuerySet[TradeOfferInCart]
        products_cost = cart.get_cart_total_sum()
        total_cost = self._map_order_products(order, products)
        order.discount_value += products_cost - total_cost
        products_weight = cart.get_weight_of_products()  # вес в граммах

        order.cost = total_cost  # стоимость продуктов в заказе
        order.delivery_cost = 0  # TODO: разобраться с стоимостью доставки
        order.summary_cost = total_cost + order.delivery_cost  # общая стоимость заказа
        order.weight = products_weight
        order.save()

        cart.status = "payed"
        cart.save(update_fields=("status",))


        transaction.on_commit(lambda: send_created_order_information.delay(order.pk))
        return order

    @classmethod
    def _map_order_products(cls, order: Order, products: QuerySet[TradeOfferInCart]):
        total_cost = 0
        for product_in_cart in products:
            product = product_in_cart.trade_offer.product  # type: Product
            product_in_order = {
                "product": product,
                "cost": product.get_current_price,
                "order": order,
                "size": product_in_cart.trade_offer.size,
                "color": product.color,
                "quantity": product_in_cart.quantity,
            }
            total_cost += product_in_order["cost"] * product_in_order["quantity"]

            ProductInOrder.objects.create(**product_in_order)
        return total_cost
