from django.urls import path

from orders.views.payments import SuccessPaymentView

app_name = "payments_urls"

urlpatterns = [
    path("success/", SuccessPaymentView.as_view(), name="success"),
]
