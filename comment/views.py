#
# class CommentFilter(django_filters.FilterSet):
#     book = django_filters.NumberFilter(field_name='book_id')
#     user = django_filters.NumberFilter(field_name='user_id')
#     book_title = django_filters.CharFilter(field_name='book.title')
#
#     class Meta(CommentSerializer.Meta):
#         pass

from comment.models import CommentSummary, Comment
from comment.serializers import CommentSerializer
from common.views import BaseModelViewSet


class CommentViewSet(BaseModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer

