from rest_framework import generics, status
from rest_framework.response import Response

from catalog.models import Product
from crm.permissions.mixins import GroupActionsPermissions
from crm.services.search import GlobalSearch


class GlobalSearchAPIView(generics.GenericAPIView):
    """
    @query_param search is required
    ?&search=string
    """

    http_method_names = ["get"]
    queryset = Product.objects.all()
    permission_classes = [GroupActionsPermissions]

    def get(self, request, *args, **kwargs):
        if not request.query_params.get("search"):
            return Response("search query param is required", status=status.HTTP_400_BAD_REQUEST)
        search_query = request.query_params.get("search")
        data = GlobalSearch().search(search_query)
        return Response(data, status=status.HTTP_200_OK)
