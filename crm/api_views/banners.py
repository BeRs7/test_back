from rest_framework import status
from rest_framework.response import Response

from crm.api_views.mixins import GroupActionsMixin
from utils.models import SecondBanner, MainBanner


class DeleteLookBooksView(GroupActionsMixin):
    banner = None

    def post(self, request, *args, **kwargs):
        serializer = self.get_validated_data(request)
        self.banner.objects.filter(id__in=serializer.data.get("items_to_action")).delete()
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteSecondBannerView(DeleteLookBooksView):
    banner = SecondBanner


class DeleteMainBannerView(DeleteLookBooksView):
    banner = MainBanner
