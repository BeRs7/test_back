from rest_framework import generics

from utils.models import MainBanner, SecondBanner
from utils.serializers import MainBannerSerializer, SecondBannerSerializer

app_name = "banners"


class MainBannerListView(generics.ListAPIView):
    """
    Список баннеров для главной
    """

    serializer_class = MainBannerSerializer
    queryset = MainBanner.objects.banners_for_show()


class SaleBannerListView(generics.ListAPIView):
    """"""

    serializer_class = SecondBannerSerializer
    queryset = SecondBanner.objects.banners_for_show()
