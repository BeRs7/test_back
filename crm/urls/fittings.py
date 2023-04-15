from django.urls import path

from crm.views.fittings import CRMFittingsListView, CRMFittingUpdateView

app_name = "fittings"

urlpatterns = [
    path("list/", CRMFittingsListView.as_view(), name="list"),
    path("detail/<pk>/", CRMFittingUpdateView.as_view(), name="detail"),
]
