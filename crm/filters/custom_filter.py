from django.http import QueryDict


class CustomFilter(object):
    @staticmethod
    def _get_has_filter_from_checkboxes(filters_data: QueryDict, args: list) -> bool:
        """
        Ф-ция для определения того, есть ли применённые фильтры по чекбоксам для корректного отображения
        стилей в фильтрах CRM
        """
        for item in args:
            if filters_data.get(item, None):
                return True
        return False
