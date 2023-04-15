from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer

from utils.files.serializers import CropImageFieldSerializer
from utils.models import Banner404


class Page404DetailSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Banner404)
    desktop_image = CropImageFieldSerializer("2880x1400", options={"crop": "center"})
    mobile_image = CropImageFieldSerializer("1400x950", options={"crop": "center"})

    class Meta:
        model = Banner404
        fields = [
            "translations",
            "desktop_image",
            "mobile_image",
            # "button_left_link",
            # "button_right_link",
            # "button_left_color",
            # "button_right_color",
            # "button_left_text_color",
            # "button_right_text_color",
        ]
