from subscriptions.models import SizeSubscription, EmailNewsletter
from utils.filters import BaseFilter


class CRMSizeSubscriptionsFilter(BaseFilter):
    searching_fields = ("id", "user__email", "email", "phone", "product__translations__name", "product__sku")

    class Meta:
        model = SizeSubscription
        fields = ["id", "user", "email", "phone", "product"]


class CRMEmailNewsletterView(BaseFilter):
    searching_fields = ("id", "user__email", "email")

    class Meta:
        model = EmailNewsletter
        fields = ["id", "user", "email"]
