from django.urls import path

from orders.views import FittingRegistrationCreateAPIView
from orders.views.fittings import AvailableFittingsAPIView

urlpatterns = [
    path("register/", FittingRegistrationCreateAPIView.as_view(), name="register"),
    path("available-list/", AvailableFittingsAPIView.as_view(), name="available-list"),
]
