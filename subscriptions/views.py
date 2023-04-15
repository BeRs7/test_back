# Create your views here.
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from subscriptions.helpers import subscribe_activation_token
from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionCreateSerializer
from rest_framework import generics


class SubscriptionViewSet(ModelViewSet):
    queryset = Subscription.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "create":
            return SubscriptionCreateSerializer


class SubscriptionActivationView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        uidb64 = self.kwargs.get("uidb64")
        token = self.kwargs.get("token")
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            subscription = Subscription.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Subscription.DoesNotExist):
            subscription = None
        if subscription and subscribe_activation_token.check_token(subscription, token):
            subscription.is_active = True
            subscription.save()
            return Response({"activation": "success"})
        else:
            return Response({"activation": "Activation link is invalid!"})
