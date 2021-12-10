from rest_framework.pagination import PageNumberPagination


class RecipeViewSetPagination(PageNumberPagination):
    page_size_query_param = 'limit'
