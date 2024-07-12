from rest_framework import pagination
from rest_framework.response import Response

class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "current_page": self.page.number,
            "total_pages": self.page.paginator.num_pages,
            "total_items": self.page.paginator.count,
            "items_per_page": self.page_size,
            "results": data
        })
    