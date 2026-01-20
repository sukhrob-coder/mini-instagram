from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 200

    def paginate_queryset(self, queryset, request, view=None):
        self.page_size = self.get_page_size(request)
        if not self.page_size:
            return None

        paginator = self.django_paginator_class(queryset, self.page_size)
        requested_page = request.query_params.get(self.page_query_param, 1)

        try:
            requested_page = int(requested_page)
        except (TypeError, ValueError):
            requested_page = 1

        if requested_page > paginator.num_pages:
            requested_page = paginator.num_pages if paginator.num_pages > 0 else 1

        try:
            self.page = paginator.page(requested_page)
        except Exception:
            raise NotFound("Page not valid.")

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        pages_number = self.page.paginator.num_pages
        return Response(
            {
                "data": data,
                "pages_number": pages_number,
            }
        )
