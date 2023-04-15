from rest_framework.response import Response
from rest_framework.views import APIView

from utils.city_finder import CityByIpFinder
from utils.models import City


class DetectGeoView(APIView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        city = request.session.get("city", None)
        data = {}
        if city and city.get("id"):
            city_object = City.objects.filter(id=city.get("id")).first()
            if city_object:
                data = {
                    "id": city_object.id,
                    "ru_name": city_object.ru_name,
                    "en_name": city_object.en_name,
                    "provider": "database",
                    "country": city_object.country,
                    "iso": city_object.iso,
                    "zip_code": city_object.zip_code,
                }
        else:
            detector_data = CityByIpFinder(request.ip).detect()
            if detector_data:
                data = detector_data

        if not data:
            city = City.objects.filter(ru_name="Москва").first()
            if city:
                data = {
                    "id": city.id,
                    "en_name": "Moscow",
                    "ru_name": "Москва",
                    "provider": "default",
                    "country": "Россия",
                    "iso": "RU",
                    "zip_code": "101000",
                }
            else:
                data = {
                    "id": None,
                    "en_name": "Moscow",
                    "ru_name": "Москва",
                    "provider": "default",
                    "country": "Россия",
                    "iso": "RU",
                    "zip_code": "101000",
                }

        request.session["city"] = data

        return Response(data)
