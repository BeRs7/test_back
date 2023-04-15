from datetime import datetime
from pytz import timezone
from django.conf import settings

from rest_framework import views, status
from rest_framework.response import Response

from orders.choices.order import PaymentStatusChoices, PaymentTypeChoices, StatusChoices
from orders.models import Order


class SuccessPaymentView(views.APIView):
    http_method_names = ("post",)

    def post(self, request):
        # order = Order.objects.get(id=request.data.get("LMI_PAYMENT_NO"))
        # tz = timezone(settings.TIME_ZONE)
        # order.payment_status = PaymentStatusChoices.PAYED
        # order.payment_type = PaymentTypeChoices.CARD
        # order.status = StatusChoices.PREPAYED
        # order.paid_amount = request.data.get("LMI_PAID_AMOUNT")
        # order.paid_currency = request.data.get("LMI_PAID_CURRENCY")
        # order.payment_date = tz.fromutc(datetime.fromisoformat(request.data.get("LMI_SYS_PAYMENT_DATE")))
        # order.payment_id = request.data.get("LMI_SYS_PAYMENT_ID")
        # order.payer_ip_address = request.data.get("LMI_PAYER_IP_ADDRESS")
        # order.save()
        #
        # if bool(order.cart):
        #     cart = order.cart
        #     cart.status = "payed"
        #     cart.save(update_fields=("status",))

        return Response(status=status.HTTP_200_OK)
