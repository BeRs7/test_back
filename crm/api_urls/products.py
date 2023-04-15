from django.urls import path

from crm.api_views.products import (
    DisableProductsView,
    EnableProductsView,
    DeleteProductsView,
    CopyProductsView,
    ProductUpdateView,
)

app_name = "products"

urlpatterns = [
    path("disable/", DisableProductsView.as_view(), name="disable-products"),
    path("enable/", EnableProductsView.as_view(), name="enable-products"),
    path("delete/", DeleteProductsView.as_view(), name="delete-products"),
    path("copy/", CopyProductsView.as_view(), name="copy-products"),
    path("update/<pk>/", ProductUpdateView.as_view(), name="update"),
]
