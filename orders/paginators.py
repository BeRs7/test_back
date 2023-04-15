from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class OrderListPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "results": data,
                "num_page": self.page.paginator.num_pages,
            }
        )
