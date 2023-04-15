from django.db import transaction
from rest_framework import serializers
from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer


from cart.models import Cart, TradeOfferInCart
from catalog.models import Product, TradeOffer
from django.utils.translation import gettext_lazy as _

from catalog.serializers import (
    ImageSerializer,
    ColorSerializer,
    ProductColorSerializer,
    CategorySerializer,
)
from catalog.serializers.size import TradeOfferSizeSerializer


class ProductInCartDetailSerializer(TranslatableModelSerializer):
    images = ImageSerializer(many=True)
    translations = TranslatedFieldsField(shared_model=Product)
    color = ColorSerializer()
    colors = ProductColorSerializer(many=True)
    major_category = CategorySerializer()

    class Meta:
        model = Product
        fields = [
            "id",
            "images",
            "translations",
            "major_category",
            "color",
            "colors",
            "slug",
            "is_new",
            "price",
            "price_with_sale",
            "sku",
        ]

        read_only_fields = fields


class TradeOfferInCartSerializer(TranslatableModelSerializer):
    product = ProductInCartDetailSerializer(source="trade_offer.product")
    size = TradeOfferSizeSerializer(source="trade_offer")
    quantity = serializers.IntegerField()

    class Meta:
        model = TradeOfferInCart
        fields = [
            "size",
            "product",
            "quantity",
        ]
        read_only_fields = fields


class CartSerializer(serializers.ModelSerializer):
    products = TradeOfferInCartSerializer(many=True)

    class Meta:
        model = Cart
        fields = ("products",)


class AddToCartSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    trade_offer = serializers.PrimaryKeyRelatedField(queryset=TradeOffer.objects.active())

    class Meta:
        fields = ("trade_offer", "amount")

    @staticmethod
    def validate_max_amount(actual_amount, new_amount):
        if new_amount > actual_amount:
            raise serializers.ValidationError(
                {"error": _("Неверное количество товара"), "actual_amount": actual_amount}
            )

    def validate(self, attrs):
        attrs = super(AddToCartSerializer, self).validate(attrs)
        self.validate_max_amount(actual_amount=attrs["trade_offer"].amount, new_amount=attrs["amount"])

        return attrs

    @transaction.atomic
    def save(self, **kwargs):
        trade_offer = self.validated_data.get("trade_offer")  # type: TradeOffer
        cart = Cart.get_cart_from_request(self.context.get("request"))  # type: Cart
        cart.add_to_cart(trade_offer, self.validated_data["amount"])
        self.validate_max_amount(
            actual_amount=trade_offer.amount, new_amount=cart.get_trade_offer_in_cart(trade_offer).quantity
        )
        self.context.get("request").session["cart"] = cart.pk
        self.validated_data["cart"] = Cart.get_cart_from_request(self.context.get("request"))

    @property
    def data(self):
        return CartSerializer(instance=self.validated_data.get("cart", None), context=self.context).data


class RemoveFromCartSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    trade_offer = serializers.PrimaryKeyRelatedField(queryset=TradeOffer.objects.all())

    class Meta:
        fields = ["trade_offer", "amount"]

    def save(self, **kwargs):
        product = self.validated_data.get("trade_offer")  # type: TradeOffer
        cart = Cart.get_cart_from_request(self.context.get("request"))  # type: Cart
        cart.remove_from_cart(product, self.validated_data["amount"])
        self.context.get("request").session["cart"] = cart.pk
        self.validated_data["cart"] = Cart.get_cart_from_request(self.context.get("request"))

    @property
    def data(self):
        return CartSerializer(instance=self.validated_data.get("cart", None), context=self.context).data
