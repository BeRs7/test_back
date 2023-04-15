from django.urls import path

from cart.views.cart import AddToCartAPIView, CartListAPIView, RemoveFromCartCartAPIView

app_name = "cart_urls"

urlpatterns = [
    path("add/", AddToCartAPIView.as_view(), name="add"),
    path("remove/", RemoveFromCartCartAPIView.as_view(), name="add"),
    path("list/", CartListAPIView.as_view(), name="list"),
]
