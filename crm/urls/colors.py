from django.urls import path

from crm.views.colors import (
    CRMColorsListView,
    CRMColorCreateView,
    CRMColorUpdateView,
    CRMColorToggleActiveView, CRMColorDeleteView,
)

app_name = "colors"

urlpatterns = [
    path("list/", CRMColorsListView.as_view(), name="list"),
    path("create/", CRMColorCreateView.as_view(), name="create"),
    path("update/<int:pk>/", CRMColorUpdateView.as_view(), name="update"),
    path("toggle-is-active/<int:pk>/", CRMColorToggleActiveView.as_view(), name="toggle-is-active"),
    path("delete/<int:pk>/", CRMColorDeleteView.as_view(), name="delete"),
]
