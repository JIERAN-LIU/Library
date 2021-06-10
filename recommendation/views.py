from rest_framework import permissions, mixins
from rest_framework.viewsets import GenericViewSet

from book.models import Book
from book.serializers import BookSerializer
from comment.models import CommentSummary
from common.views import LibraryPagination
from recommendation.models import Recommendation


class BookRecommendation(mixins.ListModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookSerializer
    pagination_class = LibraryPagination
    queryset = Book.objects.all()