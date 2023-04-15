from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from users.serializers.cities import CitiesListSerializer, SetCitySerializer
from utils.models import City


class UserCityViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    permission_classes = [AllowAny]
    queryset = City.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CitiesListSerializer
        elif self.action == "create":
            return SetCitySerializer

    def get_queryset(self):
        return [City.objects.filter(ru_name="Москва").first(), City.objects.filter(ru_name="Санкт-Петербург").first()]
