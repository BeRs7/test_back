from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from utils.choices import CategoryBlockLocation
from utils.models import Banner404, CategoryBlock
from utils.serializers.category_block import CategoryBlockSerializer
from utils.serializers.page_404 import Page404DetailSerializer


class Page404DetailView(RetrieveAPIView):
    queryset = Banner404.objects.all()
    permission_classes = [AllowAny]
    serializer_class = Page404DetailSerializer

    def get(self, request, *args, **kwargs):
        ctx = self.get_serializer_context()
        result = {
            "banner": self.get_serializer(self.get_queryset(), many=True, context=ctx).data,
            "categories": CategoryBlockSerializer(
                CategoryBlock.objects.filter(location=CategoryBlockLocation.PAGE_404), many=True, context=ctx
            ).data,
        }
        return Response(result)
