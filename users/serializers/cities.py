from django.db.models import Q
from rest_framework import serializers

from utils.models import City


class CitiesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class SetCitySerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), required=False, allow_empty=True)
    ru_name = serializers.CharField(required=False, allow_blank=True)
    en_name = serializers.CharField(required=False, allow_blank=True)
    iso = serializers.CharField()
    zip_code = serializers.CharField()

    class Meta:
        model = City
        fields = [
            "ru_name",
            "en_name",
            "iso",
        ]

    def __init__(self, *args, **kwargs):
        super(SetCitySerializer, self).__init__(*args, **kwargs)
        self.city = None

    def validate(self, attrs):
        attrs = super(SetCitySerializer, self).validate(attrs)
        if not attrs.get("ru_name") and not attrs.get("en_name") and not attrs.get("id"):
            raise serializers.ValidationError(
                {"ru_name": "Не указано название города", "en_name": "Не указано название города"}
            )

        return attrs

    def save(self, **validated_data):
        validated_data = self.validated_data
        request = self.context["request"]
        if not validated_data.get("id", None):
            filter_data = (
                {"ru_name": validated_data.get("ru_name")}
                if validated_data.get("ru_name")
                else {"en_name": validated_data.get("en_name")}
            )

            city = City.objects.filter(Q(**filter_data) & Q(iso=validated_data["iso"])).first()
        else:
            city = validated_data["id"]
        if city:
            if validated_data.get("zip_code"):
                city.zip_code = validated_data.get("zip_code")
                city.save(update_fields=("zip_code",))
            request.session["city"] = {
                "id": city.id,
                "ru_name": city.ru_name,
                "en_name": city.en_name,
                "provider": "database",
                "country": city.country,
                "iso": city.iso,
                "zip_code": city.zip_code,
            }
        else:
            city = City.objects.create(**validated_data)
            request.session["city"] = {
                "id": city.id,
                "ru_name": city.ru_name,
                "en_name": city.en_name,
                "provider": "database",
                "country": city.country,
                "iso": city.iso,
                "zip_code": city.zip_code,
            }
        self.city = city
        return city

    @property
    def data(self):
        return {
            "id": self.city.id,
            "ru_name": self.city.ru_name,
            "en_name": self.city.en_name,
            "provider": "database",
            "country": self.city.country,
            "iso": self.city.iso,
            "zip_code": self.city.zip_code,
        }
