from django.urls import path

from crm.api_views.categories import (
    DisableCategoriesView,
    EnableCategoriesView,
    DeleteCategoriesView,
    CopyCategoriesView,
)

app_name = "categories"

urlpatterns = [
    path("disable/", DisableCategoriesView.as_view(), name="disable-categories"),
    path("enable/", EnableCategoriesView.as_view(), name="enable-categories"),
    path("delete/", DeleteCategoriesView.as_view(), name="delete-categories"),
    path("copy/", CopyCategoriesView.as_view(), name="copy-categories"),
]
