from rest_framework.pagination import PageNumberPagination


class LimitQueryParamPagination(PageNumberPagination):
    page_size_query_param = 'limit'
