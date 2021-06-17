from drf_haystack.filters import HaystackAutocompleteFilter
from drf_haystack.viewsets import HaystackViewSet
from rest_framework import permissions

from book.models import Book, Author, Publisher
from common.views import LibraryPagination


class BookSearchViewSet(HaystackViewSet):
    pagination_class = LibraryPagination
    index_models = [Book]
    permission_classes = [permissions.IsAuthenticated]
    filter_fields = ('text',)

