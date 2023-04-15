from django.urls import path

from crm.views.products import (
    CRMProductsListView,
    CRMProductDisableView,
    CRMProductEnableView,
    CRMProductUpdateView,
    CRMProductDeleteView,
    CRMProductCreateView,
)

app_name = "products"

urlpatterns = [
    path("list/", CRMProductsListView.as_view(), name="products-list"),
    path("detail/<pk>/", CRMProductUpdateView.as_view(), name="product-detail"),
    path("create/", CRMProductCreateView.as_view(), name="product-create"),
    path("delete/<pk>/", CRMProductDeleteView.as_view(), name="product-delete"),
    path("deactivate/<pk>/", CRMProductDisableView.as_view(), name="product-disable"),
    path("activate/<pk>/", CRMProductEnableView.as_view(), name="product-enable"),
]
