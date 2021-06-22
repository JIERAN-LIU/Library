from drf_haystack.filters import HaystackAutocompleteFilter
from drf_haystack.viewsets import HaystackViewSet
from rest_framework import permissions

from book.models import Book, Author, Publisher
from common.views import LibraryPagination
from search.serializers import BookIndexSerializer, BookAutocompleteSerializer, AuthorIndexSerializer, \
    PublisherIndexSerializer


class BookSearchViewSet(HaystackViewSet):
    pagination_class = LibraryPagination
    index_models = [Book]
    serializer_class = BookIndexSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_fields = ('text',)


class BookAutocompleteSearchViewSet(HaystackViewSet):
    pagination_class = LibraryPagination

    index_models = [Book]
    serializer_class = BookAutocompleteSerializer
    filter_backends = [HaystackAutocompleteFilter]
    permission_classes = [permissions.IsAuthenticated]
    filter_fields = ('q',)


class AuthorSearchViewSet(HaystackViewSet):
    pagination_class = LibraryPagination

    index_models = [Author]
    serializer_class = AuthorIndexSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_fields = ('text',)


class PublisherSearchViewSet(HaystackViewSet):
    pagination_class = LibraryPagination
    index_models = [Publisher]
    serializer_class = PublisherIndexSerializer
    permission_classes = [permissions.IsAuthenticated]
