from django.urls import path, include

from crm.api_views.search import GlobalSearchAPIView

app_name = "api"

urlpatterns = [
    path("products/", include("crm.api_urls.products")),
    path("categories/", include("crm.api_urls.categories")),
    path("orders/", include("crm.api_urls.orders")),
    path("users/", include("crm.api_urls.users")),
    path("global-search/", GlobalSearchAPIView.as_view(), name="global-search"),
    path("banners/", include("crm.api_urls.banners")),
]
