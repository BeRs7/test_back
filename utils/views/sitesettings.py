from rest_framework import generics

from utils.models.site_settings import SiteSettings
from utils.serializers.site_settings import SiteSettingsSerializer


class SiteSettingsAPIView(generics.RetrieveAPIView):
    serializer_class = SiteSettingsSerializer
    queryset = SiteSettings.objects.all()

    def get_object(self):
        return SiteSettings.get_solo()
