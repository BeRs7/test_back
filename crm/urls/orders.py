from django.urls import path

from crm.views.orders import CRMOrderListView, CRMOrderUpdateView

# CRMOrderSendToRetailView

app_name = "orders"

urlpatterns = [
    path("list/", CRMOrderListView.as_view(), name="list"),
    path("detail/<pk>/", CRMOrderUpdateView.as_view(), name="detail"),
    # path("send-to-retail/<pk>/", CRMOrderSendToRetailView.as_view(), name="send-to-retail"),
]
