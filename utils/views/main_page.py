from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from catalog.models import Category, Product
from catalog.serializers import ProductListSerializer
from catalog.serializers.categories import CategoryHeaderSerializer
from utils.models import MainBanner, SecondBanner
from utils.serializers import MainBannerSerializer, SecondBannerSerializer


class MainPageView(APIView):
    """
    View для главной страницы
    """

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {"request": self.request, "format": self.format_kwarg, "view": self}

    def get(self, request, *args, **kwargs):
        ctx = self.get_serializer_context()
        main_banners = MainBanner.objects.banners_for_show()
        main_banners_serializer = MainBannerSerializer(main_banners, many=True, context=ctx)
        second_banner = SecondBanner.objects.banners_for_show()
        second_banner_serializer = SecondBannerSerializer(
            second_banner, many=True, context=self.get_serializer_context()
        )
        new_products = Product.objects.catalog_list_qs().filter(is_new=True)
        new_products_serializer = ProductListSerializer(new_products, many=True, context=ctx)
        categories = Category.objects.active().filter(parent__isnull=True).order_by('order')
        categories_serializer = CategoryHeaderSerializer(categories, many=True, context=ctx)

        data = {
            "main_banners": main_banners_serializer.data,
            "second_banner": second_banner_serializer.data,
            "categories": categories_serializer.data,
            "new_products": new_products_serializer.data,
        }

        return Response(data, status=status.HTTP_200_OK)
