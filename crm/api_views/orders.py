from rest_framework import status
from rest_framework.response import Response

from crm.api_views.mixins import GroupActionsMixin
from crm.services.orders import OrderHelper


class DeleteOrdersView(GroupActionsMixin):
    def post(self, request, *args, **kwargs):
        serializer = self.get_validated_data(request)
        OrderHelper().delete_orders(serializer.data.get("items_to_action"))
        return Response(serializer.data, status=status.HTTP_200_OK)


class CopyOrdersView(GroupActionsMixin):
    def post(self, request, *args, **kwargs):
        serializer = self.get_validated_data(request)
        OrderHelper().copy_orders(serializer.data.get("items_to_action"))
        return Response(serializer.data, status=status.HTTP_200_OK)


# class SendOrderToRetailView(GroupActionsMixin):
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_validated_data(request)
#         OrderHelper().send_orders_to_retail(serializer.data.get("items_to_action"))
#         return Response(serializer.data, status=status.HTTP_200_OK)
