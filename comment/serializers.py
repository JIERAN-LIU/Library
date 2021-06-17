from rest_framework import serializers

from comment.models import Comment, CommentSummary


class CommentSerializer(serializers.ModelSerializer):
    book_info = serializers.SerializerMethodField(read_only=True)
    user_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_info', 'book', 'book_info', 'content', 'rating', 'created_at']
        extra_kwargs = {
            'user': {'write_only': True},
            'book': {'write_only': True}
        }

    @staticmethod
    def get_book_info(obj):
        book = obj.book
        if not book:
            book = Comment.objects.get(id=obj.id).book
        return {'id': book.id, 'title': book.title, 'cover': book.cover} if book else {}

    @staticmethod
    def get_user_info(obj):
        user = obj.user
        if not user:
            user = Comment.objects.get(id=obj.id).user
        return {'id': user.id, 'name': user.nickname or user.username, 'avatar': user.avatar} if user else {}


class CommentSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentSummary
        fields = ['id', 'book', 'rating', 'rating_number']
