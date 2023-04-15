from django.urls import path

from subscriptions.views import SubscriptionViewSet, SubscriptionActivationView

subscription_crud = SubscriptionViewSet.as_view({"post": "create"})

app_name = "subscriptions"

urlpatterns = [
    path("", subscription_crud),
    path("activate/<uidb64>/<token>/", SubscriptionActivationView.as_view(), name="subscription_activate"),
]
