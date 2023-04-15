from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer

from utils.files.serializers import CropImageFieldSerializer
from utils.models import MainBanner, SecondBanner, Banner404


class MainBannerSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=MainBanner)
    desktop_image = CropImageFieldSerializer(
        "2400",
        options={"crop": "center", "quality": 100},
    )
    mobile_image = CropImageFieldSerializer(
        "1200",
        options={"crop": "center", "quality": 100},
    )

    class Meta:
        model = MainBanner
        fields = ("desktop_image", "mobile_image", "link", "translations")


class SecondBannerSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=SecondBanner)
    desktop_image = CropImageFieldSerializer(
        "2400",
        options={"crop": "center", "quality": 100},
    )
    mobile_image = CropImageFieldSerializer(
        "1200",
        options={"crop": "center", "quality": 100},
    )

    class Meta:
        model = SecondBanner
        fields = ("desktop_image", "mobile_image", "link", "translations")


class Banner404Serializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Banner404)

    class Meta:
        model = Banner404
        fields = ["translations"]
