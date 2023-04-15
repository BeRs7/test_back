from django.urls import path

from catalog.views.categories import CategoriesOnTransactionsView, CategoriesOnMainView

app_name = "catalog_categories"

urlpatterns = [
    path("on_transactions/", CategoriesOnTransactionsView.as_view(), name="on-transactions"),
    path("main/", CategoriesOnMainView.as_view(), name="on-main"),
]
