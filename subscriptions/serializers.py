from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers

from config import settings
from subscriptions.helpers import subscribe_activation_token
from subscriptions.models import Subscription
from django.utils.translation import gettext_lazy as _

from utils.mail import send_email


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["email"]

    def create(self, validated_data):
        subscription = Subscription.objects.create(**validated_data)
        mail_subject = _("Подтвердите подписку")
        ctx = {
            "domain": settings.SITE_DOMAIN,
            "uid": urlsafe_base64_encode(force_bytes(subscription.id)),
            "token": subscribe_activation_token.make_token(subscription),
        }
        send_email(
            mail_subject,
            "subscriptions/confirm_subscription.html",
            ctx,
            [subscription.email],
        )
        return subscription
