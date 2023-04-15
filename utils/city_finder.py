"""
Пакет определяющий город по IP
"""
from typing import Optional

from dadata import Dadata
from django.conf import settings
from utils.models import City


class CityByIpFinder:
    def __init__(self, ip: str):
        self.ip = ip

    def get_by_dadata(self) -> Optional[dict]:
        dadata = Dadata(settings.DADATA_TOKEN)

        return dadata.iplocate(self.ip)

    def detect(self) -> Optional[dict]:
        provider = "default"
        kwarg = "ru_name"
        value = "Москва"
        zip_code = None
        try:
            dadata_response = self.get_by_dadata()
        except Exception:
            dadata_response = None
        if dadata_response:
            provider = "dadata"
            kwarg = "ru_name"
            value = dadata_response["data"]["city"]
            zip_code = dadata_response["data"]["postal_code"]
        if provider == "dadata":
            filter_data = {kwarg: value}
            db_city = City.objects.filter(**filter_data).first()
            if db_city:
                if not bool(db_city.zip_code) and bool(zip_code):
                    db_city.zip_code = zip_code
                    db_city.save(update_fields=("zip_code",))
                return {
                    "id": db_city.id,
                    "ru_name": db_city.ru_name,
                    "en_name": "",
                    "provider": provider,
                    "country": db_city.country,
                    "iso": db_city.iso,
                    "zip_code": db_city.zip_code,
                }
            else:
                db_city = City.objects.create(
                    ru_name=dadata_response["data"]["city"],
                    country=dadata_response["data"]["country"],
                    iso=dadata_response["data"]["country_iso_code"],
                    zip_code=dadata_response["data"]["postal_code"],
                )
                return {
                    "id": db_city.id,
                    "ru_name": db_city.ru_name,
                    "en_name": "",
                    "provider": provider,
                    "country": db_city.country,
                    "iso": db_city.iso,
                    "zip_code": db_city.zip_code,
                }

        else:
            return None
