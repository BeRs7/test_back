from django.urls import path, include

from catalog.views.catalog import (
    ProductListApiView,
    ProductDetailApiView,
    FilterListApiView,
)

app_name = "catalog_urls"

urlpatterns = [
    path("list/", ProductListApiView.as_view(), name="list"),
    path("detail/<slug:product_slug>/", ProductDetailApiView.as_view(), name="detail"),
    path("filters/list/", FilterListApiView.as_view(), name="filters_list"),
    path("categories/", include("catalog.urls.categories")),
]
