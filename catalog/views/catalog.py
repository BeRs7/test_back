from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.filters import CatalogFilter
from catalog.models import Product, Color, Size, ProductTag
from catalog.models.specs import Material
from catalog.paginators import CatalogListPagination
from catalog.serializers.filters import (
    ColorFilterSerializer,
    SizeFilterSerializer,
    TagFilterSerializer, MaterialFilterSerializer,
)
from catalog.serializers.product import ProductListSerializer, ProductDetailSerializer


class ProductListApiView(generics.ListAPIView):

    queryset = Product.objects.catalog_list_qs()
    permission_classes = [AllowAny]
    pagination_class = CatalogListPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CatalogFilter
    filterset_fields = (
        "price",
        "search",
        "category",
        "size",
        "sleeve",
        "color",
        "brand",
        "tag",
        "ordering",
        "search",
    )
    serializer_class = ProductListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if len(queryset) == 0 and "search" in request.query_params:
            # если во время поиска ничего не найдено, то возвращать 8 продуктов из новинок
            queryset = Product.objects.catalog_list_qs().filter(is_new=True)[:8]
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {
                    "count": len(queryset),
                    "results": serializer.data,
                    "num_page": 1,
                    "nothing_found": True,
                }
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductDetailApiView(generics.RetrieveAPIView):

    queryset = Product.objects.catalog_list_qs()
    permission_classes = [AllowAny]
    lookup_url_kwarg = "product_slug"
    lookup_field = "slug"
    serializer_class = ProductDetailSerializer


class FilterListApiView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        response = {
            "filter_color": ColorFilterSerializer(
                Color.objects.filter(display_on_main=True).prefetch_related("translations"), many=True
            ).data,
            "filter_size": SizeFilterSerializer(
                Size.objects.filter(display_on_main=True).prefetch_related("translations"), many=True
            ).data,
            "filter_tag": TagFilterSerializer(
                ProductTag.objects.filter(is_active=True).prefetch_related("translations"), many=True
            ).data,
            "filter_material": MaterialFilterSerializer(
                Material.objects.filter(display_on_main=True).prefetch_related("translations"), many=True
            ).data,
        }

        return Response(response)
