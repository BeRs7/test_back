from django.urls import path

from crm.api_views.orders import DeleteOrdersView, CopyOrdersView

# SendOrderToRetailView

app_name = "orders"

urlpatterns = [
    path("delete/", DeleteOrdersView.as_view(), name="delete-orders"),
    path("copy/", CopyOrdersView.as_view(), name="copy-orders"),
    # path("send-to-retail/", SendOrderToRetailView.as_view(), name="send-to-retail-orders"),
]
