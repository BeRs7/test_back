from rest_framework import generics
from rest_framework.permissions import AllowAny

from text_pages.models import TextPage
from text_pages.serializers import TextPageSerializer, DetailTextPageSerializer


class TextPagesListPage(generics.ListAPIView):
    queryset = TextPage.objects.filter(is_active=True).prefetch_related("translations")
    permission_classes = [AllowAny]
    serializer_class = TextPageSerializer


class TextPagesMainPage(generics.RetrieveAPIView):
    queryset = TextPage.objects.filter(is_active=True).prefetch_related("translations")
    permission_classes = [AllowAny]
    lookup_url_kwarg = "slug"
    lookup_field = "slug"
    serializer_class = DetailTextPageSerializer
