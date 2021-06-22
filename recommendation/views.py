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

    def filter_queryset(self, queryset):
        """
        Do recommendation by KNN
        k=3
        :return:
        """
        user_id = self.request.user.id
        recommendation = Recommendation()
        try:
            algo = recommendation.algo
            inner_id = algo.trainset.to_inner_iid(user_id)
            neighbors_inner_ids = algo.get_neighbors(inner_id, k=3)
            return self.get_queryset().filter(id__in=[algo.trainset.to_raw_iid(i) for i in neighbors_inner_ids])
        except ValueError as e:
            print("There is no user's recommendation")
            summaries = CommentSummary.objects.order_by('-rating_number')
            book_ids = set()
            for s in summaries[:100]:
                book_ids.add(s.book_id)
            return queryset.filter(id__in=book_ids)
