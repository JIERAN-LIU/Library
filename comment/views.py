import django_filters

from comment.models import CommentSummary, Comment
from comment.serializers import CommentSerializer
from common.views import BaseModelViewSet

#
# class CommentFilter(django_filters.FilterSet):
#     book = django_filters.NumberFilter(field_name='book_id')
#     user = django_filters.NumberFilter(field_name='user_id')
#     book_title = django_filters.CharFilter(field_name='book.title')
#
#     class Meta(CommentSerializer.Meta):
#         pass


class CommentViewSet(BaseModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        user = self.fill_user(serializer, 'create')
        user['user_id'] = serializer.context['request'].user.id
        serializer.save(**user)
        self.update_summary(serializer)

    @staticmethod
    def update_summary(serializer):
        data = serializer.validated_data
        book_id = data['book'].id
        rating = data['rating']

        summaries = CommentSummary.objects.filter(book_id=book_id)
        if len(summaries):
            summary = summaries[0]
            rating_number = summary.rating_number + 1
            summary.rating = round(((summary.rating * summary.rating_number + rating) / rating_number), 2)
            summary.rating_number = rating_number
        else:
            summary = CommentSummary(book_id=book_id, rating=rating, rating_number=1)
        summary.save()
