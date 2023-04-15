from datetime import datetime
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from catalog.services import YClientsAPI
from orders.serializers import FittingRegistrationSerializer
from orders.models import RegistrationForFitting


class FittingRegistrationCreateAPIView(generics.CreateAPIView):
    serializer_class = FittingRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        registration = serializer.save()  # type: RegistrationForFitting
        try:
            YClientsAPI().register_seance(registration)
        except Exception:
            return Response(
                data={
                    "error": True,
                    "message": "Произошла ошибка при создании записи. Попробуйте снова или обратитесь к менеджеру."
                }, status=HTTP_400_BAD_REQUEST
            )

        return Response(
            data={
                "error": False,
                "message": "Запись успешно создана"
            }, status=HTTP_201_CREATED
        )


class AvailableFittingsAPIView(APIView):
    """
    query params:
    date_from -- iso-8601
    date_to -- iso-8601
    fitting_type -- int
    (8765543, "Примерка коротких платьев"),
    (8765556, "Повторная примерка коротких платьев"),
    (8765563, "Примерка длинных платьев"),
    (8765582, "Повторная примерка длинных платьев"),
    (8765595, "Примерка сшитого платья на заказ"),
    (8765051, "Записаться на примерку"),
    """
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        if (
                request.query_params.get("date_from") is None or
                request.query_params.get("date_to") is None or
                request.query_params.get("fitting_type") is None
        ):
            return Response(
                data={
                    "error": True,
                    "message": "Один или несколько обязательных параметров не указаны: date_from, date_to, fitting_type"
                }, status=HTTP_400_BAD_REQUEST
            )
        date_from = datetime.fromisoformat(request.query_params.get("date_from").replace(" 03:00", "+03:00"))
        date_to = datetime.fromisoformat(request.query_params.get("date_to").replace(" 03:00", "+03:00"))
        service_id = int(request.query_params.get("fitting_type"))
        return Response(data=YClientsAPI().get_seances_for_interval(date_from, date_to, service_id), status=HTTP_200_OK)
