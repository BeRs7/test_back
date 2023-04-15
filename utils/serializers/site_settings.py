from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer

from utils.models.site_settings import SiteSettings


class SiteSettingsSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(
        shared_model=SiteSettings
    )

    class Meta:
        model = SiteSettings
        fields = (
            "translations",
            "yandex_market_link",
            "vk_link",
            "instagram_link",
            "site_phone",
            "site_email"
        )
