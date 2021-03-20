  
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
    )



class FleekLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 10


class FleekPageNumberPagination(PageNumberPagination):
    page_size = 20
    