from django.urls import path

from orders.views import OrderCreateApiView

urlpatterns = [
    path("create/", OrderCreateApiView.as_view(), name="create"),
]
