from django.urls import path

from crm.views.categories import (
    CRMCategoriesListView,
    CRMCategoryChangeStatus,
    CRMCategoryUpdateView,
    CRMCategoryDeleteView,
    CRMCategoryCreateView,
)

app_name = "categories"

urlpatterns = [
    path("create/", CRMCategoryCreateView.as_view(), name="category-create"),
    path("list/", CRMCategoriesListView.as_view(), name="categories-list"),
    path("detail/<pk>/", CRMCategoryUpdateView.as_view(), name="category-detail"),
    path("delete/<pk>/", CRMCategoryDeleteView.as_view(), name="category-delete"),
    path("change-status/<pk>/", CRMCategoryChangeStatus.as_view(), name="change-status"),
]
