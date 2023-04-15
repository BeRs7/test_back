from django.urls import path

from crm.views.sizes import (
    CRMSizesListView,
    CRMSizeCreateView,
    CRMSizeUpdateView,
    CRMSizeToggleActiveView, CRMSizeDeleteView,
)

app_name = "sizes"

urlpatterns = [
    path("list/", CRMSizesListView.as_view(), name="list"),
    path("create/", CRMSizeCreateView.as_view(), name="create"),
    path("update/<int:pk>/", CRMSizeUpdateView.as_view(), name="update"),
    path("toggle-is-active/<int:pk>/", CRMSizeToggleActiveView.as_view(), name="toggle-is-active"),
    path("delete/<int:pk>/", CRMSizeDeleteView.as_view(), name="delete"),
]
