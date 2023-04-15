from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from catalog.models import Category
from catalog.serializers.categories import CategoryHeaderSerializer
from text_pages.models import TextPage
from text_pages.serializers import TextPageSerializer


class GeneralAPIView(APIView):
    """
    Общее для всех страниц
    """

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {"request": self.request, "format": self.format_kwarg, "view": self}

    def get(self, request, *args, **kwargs):
        ctx = self.get_serializer_context()

        categories = Category.objects.active()
        categories_serializer = CategoryHeaderSerializer(categories, many=True, context=ctx)
        text_pages = TextPage.objects.filter(show_in_footer=True, is_active=True)
        text_pages_serializer = TextPageSerializer(text_pages, many=True, context=ctx)

        data = {
            "categories": categories_serializer.data,
            "text_pages": text_pages_serializer.data,
        }

        return Response(data, status=status.HTTP_200_OK)
