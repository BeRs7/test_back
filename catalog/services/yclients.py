import json
from typing import List

import requests
from django.conf import settings
from datetime import datetime, timedelta

from orders.models import RegistrationForFitting


class YClientsAPI:

    def __init__(self, language='ru-RU'):
        self.token = settings.YCLIENTS_TOKEN
        self.company_id = settings.YCLIENTS_COMPANY_ID
        self.form_id = settings.YCLIENTS_FORM_ID
        self.staff_id = settings.YCLIENTS_STAFF_ID
        self.headers = {
            'Accept-Language': language,
            'Authorization': "Bearer {}".format(self.token),
            'Cache-Control': "no-cache",
            'Accept': "application/vnd.yclients.v2+json",
            'Content-Type': 'application/json',
        }

    def get_seances_for_day(self, date: datetime, service_id: int) -> dict:
        """
        Получаем список доступных сеансов за день

        :param date: datetime
        :param service_id: int
        :return: dict
        """
        params = {"service_ids": [service_id]}
        response = requests.get(
            f"https://api.yclients.com/api/v1/book_times/"
            f'{self.company_id}/0/{date.date().isoformat()}',
            headers=self.headers, params=params
        )
        if response.ok and response.json().get("success", False):
            return response.json()
        return {}

    def get_seances_for_interval(self, date_from: datetime, date_to: datetime, service_id: int) -> dict:
        """
        Получаем список доступных сеансов за указанный интервал
        date_interval - [от: datetime, до: datetime]

        :param date_from: datetime
        :param date_to: datetime
        :param service_id: int
        :return: dict
        """
        days_array = [  # разбиваем интервал по дням
            (date_from + timedelta(days=days_to_add)).replace(hour=0, minute=0)  # type: datetime
            for days_to_add in [  # type: int
                days_to_add for days_to_add in range((date_to - date_from).days)
            ]
        ]
        data = {day.date().isoformat(): self.get_seances_for_day(day, service_id).get("data", {}) for day in days_array}
        return data

    def register_seance(self, registration: RegistrationForFitting) -> dict:
        """
        Создает запись на сеанс

        :param registration: RegistrationForFitting
        :return: dict
        """
        celebrate_date = registration.date_of_wedding.strftime("%d.%m.%Y")
        comment = f'{"Комментарий:" if registration.comment else ""}{registration.comment}'
        data = {
            "phone": registration.phone,
            "email": registration.email,
            "fullname": registration.full_name,
            "comment": f'Дата свадьбы: {celebrate_date}' + "\n" + comment,
            "appointments": [{
                "id": registration.pk,
                "services": [int(registration.service_type)],
                "staff_id": 0,
                "datetime": registration.time.isoformat(),
            }]
        }
        print(json.dumps(data))
        response = requests.post(
            f"https://api.yclients.com/api/v1/book_record/{self.company_id}",
            headers=self.headers, data=json.dumps(data)
        )
        if response.ok:
            response_data = response.json()
            registration.external_id = response_data["data"][0].get("id")
            registration.external_hash = response_data["data"][0].get("record_hash")
            registration.save(update_fields=("external_id", "external_hash"))
            return response.json()
        else:
            print(response.json())
            raise Warning("Ошибка при регистрации на примерку: {}".format(response.json()))
