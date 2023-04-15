from django.urls import path, include

from utils.views import DetectGeoView

urlpatterns = [
    path("users/", include("users.urls")),
    path("utils/", include("utils.urls")),
    path("catalog/", include("catalog.urls.catalog")),
    path("text-pages/", include("text_pages.urls.text_pages")),
    path("faq/", include("text_pages.urls.faq")),
    path("orders/", include("orders.urls.order")),
    path("fittings/", include("orders.urls.fittings")),
    path("payments/", include("orders.urls.payments")),
    path("cart/", include("cart.urls")),
    path("detect-geo/", DetectGeoView.as_view()),
    path("subscriptions/", include("subscriptions.urls")),
    path("select2/", include("django_select2.urls")),
]
