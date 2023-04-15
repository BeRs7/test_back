import logging
from django.conf import settings

from django.utils.translation import gettext_lazy as _
from celery import shared_task

from orders.models import Order
from utils.mail import send_email
from utils.models.contacts_emails import EmailForContacts

logger = logging.getLogger(__name__)


def get_recipient(order):
    if order.email:
        return order.email
    elif order.user:
        return order.user.email
    raise Warning("В заказе #{} не указана почта получателя.".format(order.id))


@shared_task
def send_created_order_information(order_id: int):
    order = Order.objects.filter(id=order_id).first()
    if order:
        # title: str, tpl_name: str, ctx: dict, recipients: list
        ctx = {"order": order, "domain": settings.DOMAIN}
        send_email(
            title=_("Заказ #{} успешно оформлен".format(order.id)),
            tpl_name="client_order.html",
            ctx=ctx,
            recipients=[get_recipient(order)],
        )
        managers = EmailForContacts.objects.values_list('email', flat=True)
        send_email(
            title=_("Заказ #{} оформлен".format(order.id)),
            tpl_name="manager_order_created.html",
            ctx=ctx,
            recipients=managers,
        )
    else:
        raise Warning("Заказ #{} для отправки письма не найден.".format(order_id))
