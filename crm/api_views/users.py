from django.utils.decorators import method_decorator
from rest_framework import status, generics
from rest_framework.response import Response

from crm.api_views.mixins import GroupActionsMixin
from crm.serializers.users import UserChangePassword
from crm.services.users import UserHelper
from users.models import User
from utils.decorators import crm_member_required


class DeleteUsersView(GroupActionsMixin):
    def post(self, request, *args, **kwargs):
        serializer = self.get_validated_data(request)
        UserHelper().delete_users(serializer.data.get("items_to_action"))
        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(crm_member_required, "dispatch")
class CRMChangePassowrd(generics.UpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UserChangePassword

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)