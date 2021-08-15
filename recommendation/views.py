import random

from rest_framework import permissions, mixins
from rest_framework.viewsets import GenericViewSet

from book.models import Book
from book.serializers import BookSerializer
from comment.models import CommentSummary, Comment
from common.constant import Constant
from common.views import LibraryPagination
from recommendation.models import Recommendation


class BookRecommendation(mixins.ListModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookSerializer
    pagination_class = LibraryPagination
    queryset = Book.objects.all().exclude(status=Constant.BOOK_STATUS_DELETED).select_related('publisher')

    def filter_queryset(self, queryset):
        """
        Do recommendation by KNN
        k=3
        :return:
        """
        user_id = self.request.user.id
        recommendation = Recommendation()
        try:
            books = []
            comments = list(Comment.objects.filter(user_id=user_id).filter(rating__gt=8))
            for comment in random.choices(comments, k=min(2, len(comments))):
                books.append(comment.book_id)
            algo = recommendation.algo
            raw_ids = []
            for book_id in books:
                inner_id = algo.trainset.to_inner_iid(book_id)
                neighbors_inner_ids = algo.get_neighbors(inner_id, k=3)
                for inner in neighbors_inner_ids:
                    raw_ids.append(algo.trainset.to_raw_iid(inner))

            return self.get_queryset().filter(id__in=set(raw_ids))
        except ValueError as e:
            print("There is no user's recommendation")
            summaries = CommentSummary.objects.order_by('-rating_number')
            book_ids = set()
            for s in summaries[:100]:
                book_ids.add(s.book_id)
            return queryset.filter(id__in=book_ids)
