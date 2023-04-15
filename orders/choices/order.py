from django.utils.translation import gettext_lazy as _

__all__ = (
    "StatusChoices",
    "PaymentStatusChoices",
    "PaymentTypeChoices",
    "PickupTypeChoices",
)


class StatusChoices:
    NEW = "new"
    TRANSFERRED_TO_DELIVERY = "send-to-delivery"
    DELIVERED = "dostavlen-klientu"
    COMPLETED = "complete"
    CANCELED = "cancel-other"
    RETURNED = "vozvrat"
    ASSEMBLING = "assembling"
    PREPAYED = "prepayed"
    NOT_PAYED_DELIVERY = "notpaydelivery"
    CHANGE = "change"
    ASSEMBLING_COMPLETE = "assembling-complete"
    DELIVERING = "delivering"
    REDIRECT = "redirect"
    RETURN_DELIVERY = "return-delivery"
    NO_CALL = "no-call"
    NO_PRODUCT = "no-product"
    DELIVERY_NOT_SUIT = "delyvery-did-not-suit"
    QUESTION = "question"

    CHOICES = (
        (NEW, _("Новый")),
        (TRANSFERRED_TO_DELIVERY, _("Передан в доставку")),
        (DELIVERED, _("Доставлен клиенту")),
        (CANCELED, _("Отменен")),
        (COMPLETED, _("Выполнен")),
        (RETURNED, _("Возврат")),
        (ASSEMBLING, _("Комплектуется")),
        (PREPAYED, _("Предоплата поступила")),
        (NOT_PAYED_DELIVERY, _("Доставка не оплачана")),
        (CHANGE, _("Обмен")),
        (ASSEMBLING_COMPLETE, _("Укомплектован")),
        (DELIVERING, _("Доставляется")),
        (REDIRECT, _("Доставка перенесена")),
        (RETURN_DELIVERY, _("Вовзврат отправления")),
        (NO_CALL, _("Недозвон")),
        (NO_PRODUCT, _("Нет в наличии")),
        (DELIVERY_NOT_SUIT, _("Не устроила доставка")),
        (QUESTION, _("Остались вопросы")),
    )


class PaymentStatusChoices:
    NOT_PAYED = "not-paid"
    PAYED = "paid"
    FAIL = "fail"
    RETURN = "vozvrat"

    CHOICES = (
        (NOT_PAYED, _("Не оплачено")),
        (PAYED, _("100% оплата")),
        (FAIL, _("Ошибка")),
        (RETURN, _("Возврат")),
    )


class PaymentTypeChoices:
    CARD = "card"
    UPON_RECEIPT = "upon_receipt"

    CHOICES = ((CARD, _("Онлайн")), (UPON_RECEIPT, _("Наличные при получении")))


class PickupTypeChoices:
    UNKNOWN = "unknown"
    PICKUP = "pickup"

    CHOICES = (
        (UNKNOWN, _("Другое")),
        (PICKUP, _("Самовывоз")),
    )
