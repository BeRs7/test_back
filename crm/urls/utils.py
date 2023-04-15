from django.urls import path

from crm.views.search import CRMGlobalSearchView

app_name = "utils"

urlpatterns = [
    path("global-search/", CRMGlobalSearchView.as_view(), name="global-search"),
]
