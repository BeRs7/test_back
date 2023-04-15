from rest_framework import generics
from rest_framework.response import Response

from cart.models import Cart
from cart.serializers.cart import (
    AddToCartSerializer,
    RemoveFromCartSerializer,
    CartSerializer,
)


class AddToCartAPIView(generics.CreateAPIView):
    serializer_class = AddToCartSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RemoveFromCartCartAPIView(generics.CreateAPIView):
    serializer_class = RemoveFromCartSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CartListAPIView(generics.RetrieveAPIView):
    queryset = Cart.objects.active()
    serializer_class = CartSerializer

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {"request": self.request, "format": self.format_kwarg, "view": self}

    def get_object(self):
        return Cart.get_cart_from_request(self.request)
