from rest_framework import generics
from rest_framework.permissions import AllowAny

from text_pages.models import FAQQuestion
from text_pages.serializers import FAQQuestionSerializer


class FAQQuestionsListPage(generics.ListAPIView):
    queryset = FAQQuestion.objects.filter(is_active=True).prefetch_related("translations")
    permission_classes = [AllowAny]
    serializer_class = FAQQuestionSerializer
