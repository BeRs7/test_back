from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from crm.permissions.mixins import GroupActionsPermissions
from crm.serializers.mixins import ItemsToActionSerializer


class GroupActionsMixin(generics.GenericAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication,)
    serializer_class = ItemsToActionSerializer
    permission_classes = [GroupActionsPermissions]
    http_method_names = ["post"]

    def get_validated_data(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer
