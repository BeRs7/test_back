from rest_framework import status
from rest_framework.response import Response

from crm.api_views.mixins import GroupActionsMixin
from crm.services.categories import CategoryHelper


class DisableCategoriesView(GroupActionsMixin):
    def post(self, request, *args, **kwargs):
        serializer = self.get_validated_data(request)
        CategoryHelper().disable_categories(serializer.data.get("items_to_action"))
        return Response(serializer.data, status=status.HTTP_200_OK)


class EnableCategoriesView(GroupActionsMixin):
    def post(self, request, *args, **kwargs):
        serializer = self.get_validated_data(request)
        CategoryHelper().enable_categories(serializer.data.get("items_to_action"))
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteCategoriesView(GroupActionsMixin):
    def post(self, request, *args, **kwargs):
        serializer = self.get_validated_data(request)
        CategoryHelper().delete_categories(serializer.data.get("items_to_action"))
        return Response(serializer.data, status=status.HTTP_200_OK)


class CopyCategoriesView(GroupActionsMixin):
    def post(self, request, *args, **kwargs):
        serializer = self.get_validated_data(request)
        CategoryHelper().copy_categories(serializer.data.get("items_to_action"))
        return Response(serializer.data, status=status.HTTP_200_OK)
