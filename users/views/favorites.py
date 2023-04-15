from django.db.models import Q
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from catalog.models import Product
from catalog.serializers.product import ProductListSerializer
from users.serializers.user import ToggleUserFavoriteSerializer


class FavoritesViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    permission_classes = [AllowAny]
    queryset = Product.objects.none()

    def get_serializer_class(self):
        if self.action == "create":
            return ToggleUserFavoriteSerializer
        elif self.action == "list":
            return ProductListSerializer

    def get_queryset(self):
        return Product.objects.catalog_list_qs(custom_query=Q(id__in=self.request.session.get("favorites", [])))
