
from rest_framework import pagination
from rest_framework.response import Response

class CustomPagination(pagination.CursorPagination):
    page_size_query_param = 'limit'
    max_page_size = 250
    min_page_size = 10
    ordering = '-created_at'

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
            # 'count':  self.page.paginator.count
        })
