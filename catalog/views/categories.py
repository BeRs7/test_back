from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from catalog.models import Category
from catalog.serializers import CategorySerializer, CategoryInMenuSerializer


class CategoriesOnTransactionsView(generics.ListAPIView):
    queryset = Category.objects.on_transactions()
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer


class CategoriesOnMainView(generics.ListAPIView):
    queryset = Category.objects.main()
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        category_for_display_in_menu = Category.objects.main().filter(display_in_menu=True).first()

        response_data = {
            "categories": serializer.data,
            "display_category": CategoryInMenuSerializer(
                instance=category_for_display_in_menu, many=False, context=self.get_serializer_context()
            ).data if category_for_display_in_menu else None
        }

        return Response(response_data)

