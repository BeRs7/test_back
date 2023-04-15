from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from catalog.models import Product
from crm.api_views.mixins import GroupActionsMixin
from crm.permissions.mixins import GroupActionsPermissions
from crm.serializers.mixins import ProductSerializer

from crm.services.products import ProductHelper


class DisableProductsView(GroupActionsMixin):
    authentication_classes = (SessionAuthentication, BasicAuthentication,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_validated_data(request)
        ProductHelper().disable_products(serializer.data.get("items_to_action"))
        return Response(serializer.data, status=status.HTTP_200_OK)


class EnableProductsView(GroupActionsMixin):
    authentication_classes = (SessionAuthentication, BasicAuthentication,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_validated_data(request)
        ProductHelper().enable_products(serializer.data.get("items_to_action"))
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteProductsView(GroupActionsMixin):
    authentication_classes = (SessionAuthentication, BasicAuthentication,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_validated_data(request)
        ProductHelper().delete_products(serializer.data.get("items_to_action"))
        return Response(serializer.data, status=status.HTTP_200_OK)


class CopyProductsView(GroupActionsMixin):
    authentication_classes = (SessionAuthentication, BasicAuthentication,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_validated_data(request)
        ProductHelper().copy_products(serializer.data.get("items_to_action"))
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductUpdateView(GenericAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [GroupActionsPermissions]
    http_method_names = ["post"]

    # Сделал апдейт через POST, так как с put и patch были проблемы на ajax'e
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context=self.get_serializer_context())
        serializer.is_valid()
        instance = self.get_object()
        for field, value in request.data.items():
            setattr(instance, field, value)
            instance.save(update_fields=[field])
        return Response({"success": "true"})
