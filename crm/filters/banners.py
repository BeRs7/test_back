from utils.filters import BaseFilter
from utils.models import SecondBanner, MainBanner


class CRMBannersFilter(BaseFilter):
    searching_fields = ("id", "name")

    class Meta:
        model = SecondBanner
        fields = ["id", "name"]


class CRMMainBannersFilter(BaseFilter):
    searching_fields = ("id", "name")

    class Meta:
        model = MainBanner
        fields = ["id", "name"]
